using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Client
{
    public partial class Form3 : Form
    {
        string ipAddress = "127.0.0.1";
        string port = "9050";

        private Socket client;
        byte[] buffSend = new byte[1024];
        byte[] buffReceive = new byte[1024];
        string _ma = "";
        private delegate void updateUI(string message);
        private updateUI updateUi;
        string playerName = "";
        bool inRoom = false;
        int roomNumber = 0;


        public Form3()
        {
            InitializeComponent();
            starClient();
            updateUi = new updateUI(update);
            CheckForIllegalCrossThreadCalls = false;
        }

        private void starClient()
        {
            EndPoint ipep = new IPEndPoint(IPAddress.Parse(ipAddress.ToString()), Convert.ToInt32(port.ToString()));
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            //updateUi("Đã kết nối...");
            //// thực hiện việc kết nối và gọi beginConnect
            client.BeginConnect(ipep, new AsyncCallback(beginConnect), client); // ipep của thiết bị cần kết nối tới
            // đăng ký beginConnect khi có kết nối hoàn tất. truyển client đến EndConnect

        }

        private void beginConnect(IAsyncResult ar)
        {
            try
            {
                client.EndConnect(ar);  // lấy socket của nơi gửi
                //updateUi("Kết nối thành công tới Server: " + client.RemoteEndPoint.ToString());
                string welcome = " ";
                buffSend = new byte[1024];
                buffSend = Encoding.UTF8.GetBytes(welcome);
                // đắng ký việc gửi dữ liệu
                client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);  // sendData được gọi khi phương thức BeginSend thực hiện thành công.
                // nhận  dữ liệu
                buffReceive = new byte[1024];
                client.BeginReceive(buffReceive, 0, buffReceive.Length, SocketFlags.None, new AsyncCallback(beginReceive), client);
            }
            catch (SocketException)
            {
                //updateUi("Kết nối tới Server không thành công.");
                MessageBox.Show("Kết nối đến Server không thành công");
            }
        }


        private void update(string msg)
        {

        }


        private void sendData(IAsyncResult ai)
        {
            client.EndSend(ai);
        }


        private void sendData(string data)
        {
            buffSend = new byte[1024];
            buffSend = Encoding.UTF8.GetBytes(data);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
            //updateUi("_Client: " + txtSend.Text);
        }
        private void sendCommand(string data)
        {
            buffSend = new byte[1024];
            buffSend = Encoding.UTF8.GetBytes(data);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
        }


        private void beginReceive(IAsyncResult iar)
        {
            try
            {
                Socket s = (Socket)iar.AsyncState;
                int bytesReceive = 0;
                bytesReceive = client.EndReceive(iar);
                string receive = Encoding.UTF8.GetString(buffReceive, 0, bytesReceive);
                if (receive[0] == '+')
                {
                    _ma = receive.Substring(1);
                }
                if (receive.Substring(0, 10) == "#_TCP_DNTC")
                {
                    playerName = textBox1.Text;


                }
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DNTB")
                {
                    MessageBox.Show("Tên đăng nhập hoặc mật khẩu không đúng");
                }
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DNTT")
                {
                    MessageBox.Show("Tài khoản đang được sử dụng");
                }
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DKTB")
                {
                    MessageBox.Show("Tên đăng nhập đã tồn tại");
                }
                if (receive.Length >= 10 && receive.Substring(0, 10) == "#_TCP_DKTC")
                {
                    MessageBox.Show("Đăng kí thành công");
                }
                if (receive.Length >= 11 && receive.Substring(0, 11) == "#_TCP_DMKTC")
                {
                    MessageBox.Show("Đổi mật khẩu thành công");
                }
                if (receive.Length >= 8 && receive.Substring(0, 10) == "#_TCP_FULL")
                {
                    MessageBox.Show("Phòng đã đầy");
                }
                if (receive.Length >= 8 && receive.Substring(0, 8) == "#_TCP_UD")
                {
                    //playerOfRoom[1, int.Parse(receive[8].ToString())] = int.Parse(receive[9].ToString());
                    // Infor[int.Parse(receive[8].ToString())].Text = receive[9].ToString();
                }
                if (receive.Length >= 8 && receive.Substring(0, 8) == "#_TCP_UF")
                {
                    // for (int i = 0; i < 10; i++)
                    // {
                    //  playerOfRoom[1, i] = int.Parse(receive[i + 8].ToString());
                    //Infor[i].Text = receive[i + 8].ToString();
                    //}
                }

                //  receiveCmdPlay(receive, s);

                if (receive.Length >= 9 && receive.Substring(0, 9) == "#_Chat_00")
                {
                    updateUi(receive.Substring(9));
                }
                //updateUi("Server: " + receive);
                s.BeginReceive(buffReceive, 0, buffReceive.Length, SocketFlags.None, new AsyncCallback(beginReceive), s);
            }
            catch { }
        }



        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

       

        private void button1_Click_1(object sender, EventArgs e)
        {
            if (textBox2.Text == textBox3.Text)
            {
                buffSend = new byte[1024];
                string str = "#_TCP_DK" + textBox1.Text + " " + textBox2.Text;
                buffSend = Encoding.UTF8.GetBytes(str);
                client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
                this.Close();
                Form1 form1 = new Form1();
                form1.Show();
            }
        }

       




    }
}
