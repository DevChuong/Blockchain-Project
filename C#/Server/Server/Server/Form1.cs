using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Xml;
using System.Net.NetworkInformation;

namespace Server
{
    public partial class frmServer : Form
    {
        private Socket server, client;
        Socket _sk;
        byte[] buffReceive = new byte[1024];
        byte[] buffSend = new byte[1024];
        string userSend = "";
        private delegate void updateUI(string message); 
        private updateUI updateUi;

        RoomList lstRoom = new RoomList();
        UserList lstUser = new UserList();
        List<Socket> Client = new List<Socket>();

        public frmServer()
        {
            InitializeComponent();
            
            updateUi = new updateUI(update); 
 
            CheckForIllegalCrossThreadCalls = false;
        }

        private void update(string msg)
        {
            lstDisplay.Items.Add(msg);
            lstDisplay.TopIndex = lstDisplay.Items.Count - 1;
        }

        private void startServer()
        {
            EndPoint ipep = new IPEndPoint(IPAddress.Any, 9050);    // khai báo ip và port


            //IPAddress ipAddress = getIP();
            //IPEndPoint ipEndPoint = new IPEndPoint(ipAddress, 9050);

            server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp); // tạo 1 đối tượng socket
            server.Bind(ipep);      // gán socket với địa chỉ ip và port
            server.Listen(10);
            server.BeginAccept(new AsyncCallback(beginAccept), server); // định nghĩa delegate đx dùng khi có kết nối tới. truyền tham số beginAccept vào
            updateUi("Đang lắng nghe các kết nối...");
            
        }

        private IPAddress getIP()
        {
            var host = Dns.GetHostEntry(Dns.GetHostName());
            foreach (var ip in host.AddressList)
            {
                if (ip.AddressFamily == AddressFamily.InterNetwork)
                {
                    MessageBox.Show(ip.ToString());
                    return ip;
                }
            }
            return null;
        }

        Socket socket_send;
        // được sử dụng khi có kết nối xảy ra
        
        //List<User> _User = new List<User>();
        private void beginAccept(IAsyncResult ar)  // iasyncResult truyền giá trị bất đồng bộ từ BeginAccept đến EndAccept
        {
            // ar chứ
            Socket s = (Socket)ar.AsyncState; // nhận socket ban đầu của Server . ép kiểu đối tượng qua soket
            client = s.EndAccept(ar);   // trả về socket dùng để kết nối với client trong nhận gửi data
            updateUi("Đã kết nối với " + client.RemoteEndPoint.ToString());
            

            // đăng ký nhận dữ liệu
            client.BeginReceive(buffReceive, 0, buffReceive.Length, SocketFlags.None, new AsyncCallback(beginReceive), client);
            Client.Add(client);
            socket_send = client;

            EndPoint ipep = new IPEndPoint(IPAddress.Any, 9050);    // khai báo ip và port
            server.BeginAccept(new AsyncCallback(beginAccept), server);
        }
        
        // thực hiện việc nhận dữ liệu khi có dữ liệu tới
        private void beginReceive(IAsyncResult ia)
        {

            int bytesReceive = 0;
            try
            {
                Socket s = (Socket)ia.AsyncState;
                bytesReceive = s.EndReceive(ia);
                string receive = Encoding.UTF8.GetString(buffReceive, 0, bytesReceive);
                string str = receive;

                if (receive == "exit")
                {
                    s.Close();
                }
                else
                {
                    try
                    {
                        string playerName = "";
                        // lấy tên người chơi
                        foreach (User us in lstUser.ListPlayer)
                        {
                            if (us._Socket.RemoteEndPoint.ToString() == s.RemoteEndPoint.ToString())
                            {
                                playerName = us.UserName;
                                break;
                            }
                        }
                        
                        //Kiểm tra đăng nhập
                        if (receive.Substring(0, 8) == "#_TCP_DN")
                        {
                            Check_Login(receive, s);
                        }
                        //Kiem tra dang ki
                        if (receive.Substring(0, 8) == "#_TCP_DK")
                        {
                            Check_Signin(receive, s);
                        }
                        if (receive.Substring(0, 8) == "#_TCP_IR")
                        {
                            foreach (User us in lstUser.ListPlayer)
                            {
                                if (us._Socket.RemoteEndPoint.ToString() == s.RemoteEndPoint.ToString())
                                {
                                    int roomNumber = 1;
                                    if (lstRoom.ListRoom[roomNumber].ListPlayer.Count() >= 2)
                                    {
                                        sendData("#_TCP_FULL", s);
                                    }
                                    else
                                    {
                                        lstRoom.ListRoom[roomNumber].addPlayer(us);
                                        us.RoomNumber = roomNumber;
                                        updateListView(us);
                                        updateUi(us.UserName + " đã vào phòng " + roomNumber.ToString());
                                        if (lstRoom.ListRoom[roomNumber].ListPlayer.Count() == 2)
                                        {
                                            lstRoom.ListRoom[roomNumber].ListPlayer[0].LuotDi = 1;
                                            sendData("#_TCP_LD1" + lstRoom.ListRoom[roomNumber].ListPlayer[0].UserName.ToString(), lstRoom.ListRoom[roomNumber].ListPlayer[0]._Socket);
                                            updateUi("Room" + roomNumber.ToString() + "_" + lstRoom.ListRoom[roomNumber].ListPlayer[0].UserName.ToString() + " có lượt đi " + (1).ToString());
                                            lstRoom.ListRoom[roomNumber].ListPlayer[1].LuotDi = 2;
                                            sendData("#_TCP_LD2" + lstRoom.ListRoom[roomNumber].ListPlayer[1].UserName.ToString(), lstRoom.ListRoom[roomNumber].ListPlayer[1]._Socket);
                                            updateUi("Room" + receive[8].ToString() + "_" + lstRoom.ListRoom[roomNumber].ListPlayer[1].UserName.ToString() + " có lượt đi " + (2).ToString());
                                        }

                                        us.InRoom = true;
                                        foreach (User _us in lstUser.ListPlayer)
                                        {
                                            sendData("#_TCP_UD" + receive[8].ToString() + lstRoom.ListRoom[roomNumber].playerCount(), _us._Socket);
                                        }
                                    }
                                    break;
                                }
                            }
                        }
                        if (receive.Substring(0, 8) == "#_TCP_OR")
                        {
                            foreach (User us in lstUser.ListPlayer)
                            {
                                if (us._Socket.RemoteEndPoint.ToString() == s.RemoteEndPoint.ToString())
                                {
                                    int _nr = (int.Parse(receive[8].ToString()) + 1);
                                    updateUi(us.UserName + " đã rời phòng " + _nr.ToString());
                                    us.RoomNumber = 0;
                                    updateListView(us);
                                    us.InRoom = false;
                                    lstRoom.ListRoom[int.Parse(receive[8].ToString())].ListPlayer.Remove(us);
                                    foreach (User _us in lstUser.ListPlayer)
                                    {
                                        sendData("#_TCP_UD" + receive[8].ToString() + lstRoom.ListRoom[int.Parse(receive[8].ToString())].playerCount(), _us._Socket);
                                    }
                                    break;
                                }
                            }
                        }

                        if (receive.Substring(0, 9) == "#_TCP_OUT")
                        {                            
                            if (lstUser.ListPlayer.Count > 0)
                            {
                                foreach (User user in lstUser.ListPlayer)
                                {
                                    if (user.InRoom == true)
                                    {
                                        lstRoom.ListRoom[user.RoomNumber].ListPlayer.Remove(user);
                                    }

                                    foreach (ListViewItem item in lsvListPlayer.Items)
                                    {
                                        if (item.SubItems[1].Text == user.UserName)
                                        {
                                            lsvListPlayer.Items.Remove(item);
                                        }

                                        updateUi(user.UserName + " is disconnected ...");
                                        lstUser.ListPlayer.Remove(user);


                                    }
                                }
                            }
                        }

                        if (receive.Substring(0, 8) == "#_TCP_DO")
                        {
                            Random rd = new Random();
                            int number = rd.Next(1, 7);

                            if (lstRoom.ListRoom[int.Parse(receive[9].ToString())].GiaTriXNTruoc == 0)
                            {
                                if (number == 1 || number == 6)
                                {
                                    foreach (User us in lstRoom.ListRoom[int.Parse(receive[9].ToString())].ListPlayer)
                                    {
                                        sendData("#_TCP_VA" + receive[8].ToString() + number.ToString(), us._Socket);
                                    }
                                }
                                else
                                {
                                    foreach (User us in lstRoom.ListRoom[int.Parse(receive[9].ToString())].ListPlayer)
                                    {
                                        int ld = doiLuotDi(int.Parse(receive[8].ToString()));
                                        sendData("#_TCP_VA" + ld.ToString() + number.ToString(), us._Socket);
                                    }
                                }
                                lstRoom.ListRoom[int.Parse(receive[9].ToString())].GiaTriXNTruoc = number;
                            }
                            else
                            {
                                if (number == 1 || number == 6)
                                {
                                    foreach (User us in lstRoom.ListRoom[int.Parse(receive[9].ToString())].ListPlayer)
                                    {
                                        sendData("#_TCP_VA" + receive[8].ToString() + number.ToString(), us._Socket);
                                    }
                                }
                                else
                                {
                                    foreach (User us in lstRoom.ListRoom[int.Parse(receive[9].ToString())].ListPlayer)
                                    {
                                        int ld = doiLuotDi(int.Parse(receive[8].ToString()));
                                        sendData("#_TCP_VA" + ld.ToString() + number.ToString(), us._Socket);
                                    }
                                }
                            }
                            updateUi("Room" + receive[9].ToString() + "_" + playerName + ": lắc được xí ngầu " + number.ToString());
                        }
                        if (receive.Substring(0, 8) == "#_TCP_UB")
                        {
                            string _str = "";
                            for (int i = 11; i < receive.Length; i++)
                            {
                                if (receive[i] == '_')
                                {
                                    break;
                                }
                                _str += receive[i];
                            }
                            foreach (User us in lstRoom.ListRoom[int.Parse(receive[8].ToString())].ListPlayer)
                            {
                                if (us._Socket.RemoteEndPoint.ToString() != s.RemoteEndPoint.ToString())
                                {
                                    sendData("#_TCP_UB" + receive[8].ToString() + receive[9].ToString() + receive[10].ToString() + _str, us._Socket);
                                    //MessageBox.Show("#_TCP_UB" + receive[8].ToString() + receive[9].ToString() + receive[10].ToString() + _str);
                                }
                                //sendData("#_TCP_UB" + receive[8].ToString() + receive[9].ToString() + receive[10].ToString() + _str, us._Socket);
                            }
                        }
                        if (receive.Substring(0, 8) == "#_TCP_VD")
                        {
                            foreach (User us in lstRoom.ListRoom[int.Parse(receive[8].ToString())].ListPlayer)
                            {
                                sendData("#_TCP_KQ" + playerName, us._Socket);
                            }
                        }
                        if (receive.Substring(0, 9) == "#_TCP_DMK")
                        {
                            ChangePassword(receive, s, playerName);
                        }
                        if (receive.Substring(0, 9) == "#_Chat_00")
                        {
                            updateUi(playerName + ": " + receive.Substring(9));
                            
                            for (int i = 0; i < lstUser.ListPlayer.Count; i++)
                            {
                                if (!lstUser.ListPlayer[i].InRoom)
                                {
                                    sendData("#_Chat_00" + playerName + ": " + receive.Substring(9), lstUser.ListPlayer[i]._Socket);
                                }
                            }
                             
                        }
                        if (receive.Substring(0, 8) == "#_Chat_1")
                        {
                            for (int i = 0; i < lstRoom.ListRoom[int.Parse(receive[8].ToString())].playerCount(); i++)
                            {
                                sendData("#_Chat_00" + playerName + ": " + receive.Substring(9), lstRoom.ListRoom[int.Parse(receive[8].ToString())].ListPlayer[i]._Socket);
                                updateUi("Room" + receive[8].ToString() + "_" + playerName + ": " + receive.Substring(9));
                            }
                        }
                        updateUi(s.RemoteEndPoint.ToString() + ": "+receive);
                    }
                    catch
                    {
                        updateUi("Client: " + receive);
                    }
                    
                    s.BeginReceive(buffReceive, 0, buffReceive.Length, SocketFlags.None, new AsyncCallback(beginReceive), s);
                }
            }
            catch { }
            
        }
        

        public int doiLuotDi(int ld)
        {
            if(ld == 1)
            {
                return 2;
            }
            else
            {
                return 1;
            }
        }
        private void btnStart_Click(object sender, EventArgs e)
        {
            startServer();
            timer2.Start();
        }

        
        // send data  
        private void sendText(IAsyncResult iar)
        {
            Socket s = (Socket)iar.AsyncState;
            //socket_send.EndSend(iar);
            s.EndSend(iar);
        }

        private void btnSend_Click(object sender, EventArgs e)
        {
            if(lblNguoiNhan.Text != "")
            {
                
                if(txtSend.Text != "")
                {
                    for (int i = 0; i < lstUser.playerCount(); i++)
                    {
                        if (lblNguoiNhan.Text == lstUser.ListPlayer[i].UserName)
                        {
                            _sk = lstUser.ListPlayer[i]._Socket;
                            break;
                        }
                    }
                    buffSend = new byte[1024];
                    buffSend = Encoding.UTF8.GetBytes("#_Chat_00Server: " + txtSend.Text);
                    _sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), _sk);
                    updateUi("Server -> " + lblNguoiNhan.Text + ": " + txtSend.Text);
                    txtSend.Text = "";
                    timer1.Start();
                }
                else
                {
                    MessageBox.Show("Chưa nhập nội dung tin nhắn");
                }
            }
            else
            {
                MessageBox.Show("Bạn chưa chọn người gửi !!!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void sendData(string data, Socket sk)
        {
            buffSend = new byte[1024];
            buffSend = Encoding.UTF8.GetBytes(data);
            sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
            //updateUi("Server: " + txtSend.Text);
        }
        public void Check_Login(string str, Socket sk)
        {
            string user_client = "";
            string pass_client = "";
            for (int i = 8; i < str.Length; i++)
            {
                if (str[i] == ' ')
                {
                    pass_client = str.Substring(i + 1);
                    break;
                }
                user_client += str[i];
            }

            bool checkLogIn = false;
            bool checkStt = false;
            foreach (User us in lstUser.ListPlayer)
            {
                if (us.UserName == user_client)
                {
                    checkStt = true;
                    break;
                }
            }

            if(checkStt == false)
            {
                XmlDocument docXML = new XmlDocument();
                docXML.Load("Account.xml");

                XmlNode user = docXML.SelectSingleNode("//account");
                XmlNodeList userList = user.SelectNodes("//user");


                foreach (XmlNode nd in userList)
                {
                    if (nd.Attributes != null)
                    {
                        if (nd.Attributes["id"].Value == user_client)
                        {
                            if (nd.InnerText == pass_client)
                            {
                                updateUi(user_client + " đã online");
                                User us = new User(user_client, sk);
                                lstUser.addPlayer(us);
                                buffSend = new byte[1024];
                                buffSend = Encoding.UTF8.GetBytes("#_TCP_DNTC");
                                sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
                                Thread.Sleep(200);
                                string s = "#_TCP_UF";
                                for (int i = 0; i < 10; i++)
                                {
                                    s += lstRoom.ListRoom[i].playerCount().ToString();
                                }
                                sendData(s, sk);
                                addListView(us);
                                checkLogIn = true;
                                break;
                            }
                        }
                    }
                }
                if (checkLogIn == false)
                {
                    buffSend = new byte[1024];
                    buffSend = Encoding.UTF8.GetBytes("#_TCP_DNTB");
                    sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
                }
            }
            else
            {
                buffSend = new byte[1024];
                buffSend = Encoding.UTF8.GetBytes("#_TCP_DNTT");
                sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
            }
        }

        public void Check_Signin(string str, Socket sk)
        {
            string user_client = "";
            string pass_client = "";
            for (int i = 8; i < str.Length; i++)
            {
                if (str[i] == ' ')
                {
                    pass_client = str.Substring(i + 1);
                    break;
                }
                user_client += str[i];
            }
            
            XmlDocument docXML = new XmlDocument();
            docXML.Load("Account.xml");

            XmlNode user = docXML.SelectSingleNode("//account");
            XmlNodeList userList = user.SelectNodes("//user");
            bool check = true;
            foreach (XmlNode nd in userList)
            {
                if (nd.Attributes != null)
                {
                    if (nd.Attributes["id"].Value == user_client)
                    {
                        check = false;
                        buffSend = new byte[1024];
                        buffSend = Encoding.UTF8.GetBytes("#_TCP_DKTB");
                        sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
                    }
                }
            }

            if(check == true)
            {
                XmlNode node = docXML.CreateNode(XmlNodeType.Element, "user", null);
                node.InnerText = pass_client;
                XmlAttribute id1 = docXML.CreateAttribute("id");
                id1.Value = user_client;
                node.Attributes.Append(id1);
                docXML.SelectSingleNode("account").AppendChild(node);
                docXML.Save("Account.xml");

                updateUi(user_client + " đã đăng kí thành công tài khoản");

                buffSend = new byte[1024];
                buffSend = Encoding.UTF8.GetBytes("#_TCP_DKTC");
                sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
            }
        }

        public void ChangePassword(string str, Socket sk, string name)
        {
            string pass_client = "";
            pass_client = str.Substring(9);
            XmlDocument docXML = new XmlDocument(); // tạo đối tượng xml
            docXML.Load("Account.xml"); //load file xml có sẵn
            XmlNode user = docXML.SelectSingleNode("//account"); // chọn node gốc
            XmlNodeList userList = user.SelectNodes("//user");  //lấy danh sách các node có tên user
            foreach (XmlNode nd in userList)                    // duyệt danh sách node
            {
                if (nd.Attributes != null)
                {
                    if (nd.Attributes["id"].Value == name) /// so sánh thuộc tính node với username
                    {
                        nd.InnerText = pass_client;
                        buffSend = new byte[1024];
                        buffSend = Encoding.UTF8.GetBytes("#_TCP_DMKTC");
                        sk.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendText), sk);
                        break;
                    }
                }
            }
            docXML.Save("Account.xml");
        }

        private void addListView(User us)
        {
            
            int s = lstUser.playerCount();
            string[] _str = {s.ToString(), us.UserName, us._Socket.RemoteEndPoint.ToString(), us.RoomNumber.ToString()};
            ListViewItem item = new ListViewItem(_str);
            lsvListPlayer.Items.Add(item);
        }

        private void updateListView(User us)
        {
            for(int i = 0; i < lsvListPlayer.Items.Count; i++)
            {
                if (us.UserName == lsvListPlayer.Items[i].SubItems[1].Text.ToString())
                {
                    lsvListPlayer.Items[i].SubItems[3].Text = us.RoomNumber.ToString();
                    break;
                }
            }
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            
            this.Close();
            
        }

        private void frmServer_Load(object sender, EventArgs e)
        {
            lsvListPlayer.Columns.Add("STT", 60);
            lsvListPlayer.Columns.Add("Player's name", 130);
            lsvListPlayer.Columns.Add("IP Address", 110);
            lsvListPlayer.Columns.Add("Room", 60);
        }

        private void lsvListPlayer_ItemSelectionChanged(object sender, ListViewItemSelectionChangedEventArgs e)
        {
            try
            {
                ListViewItem item = lsvListPlayer.SelectedItems[0];
                lblNguoiNhan.Text = item.SubItems[1].Text.ToString();
            }
            catch
            {

            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            lblNguoiNhan.Text = "";
            timer1.Stop();
        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            Thread threadRun = new Thread(
                delegate()
                {
                    timTimeOut();
                }
                );
            threadRun.Start();
        }

        private void timTimeOut()
        {
            if (lstUser.ListPlayer.Count > 0)
            {
                foreach (User us in lstUser.ListPlayer)
                {
                    if (!isConnected(us._Socket))
                    {
                        if(us.InRoom == true)
                        {
                            lstRoom.ListRoom[us.RoomNumber].ListPlayer.Remove(us);
                        }

                        foreach (ListViewItem item in lsvListPlayer.Items)
                        {
                            if (item.SubItems[1].Text == us.UserName)
                            {
                                lsvListPlayer.Items.Remove(item);
                            }
                        }
                        updateUi(us.UserName + " is disconnected ...");
                        lstUser.ListPlayer.Remove(us);
                        break;
                    }
                }
            }
            else
            {
                //MessageBox.Show("No connect ...");
            }
        }

        public bool isConnected(Socket s)
        {
            try
            {
                return !(s.Poll(10, SelectMode.SelectRead) && s.Available == 0);
            }
            catch(SocketException)
            {
                return false;
            }
        }

        private void lsvListPlayer_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

       

    }
}
