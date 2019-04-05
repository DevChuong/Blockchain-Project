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
    public partial class Form1 : Form
    {   
        // địa chỉ local host của máy tính
        string ipAddress = "127.0.0.1";
        // port để kết nối đến
        string port = "9050";
        //tạo socket client
        private Socket client;
        byte[] buffSend = new byte[1024];
        byte[] buffReceive = new byte[1024];
        string _ma = "";
        int count = 0;
        // cập nhật hiển thị thông tin chat
        private delegate void updateUI(string message);
        private updateUI updateUi;

        // biến lưu tên người chơi
        string playerName = "";
        bool inRoom = false;
        int roomNumber = 0;


        public Form1()
        {
            InitializeComponent();
            // khởi tạo kết nối
            starClient();
            // cập nhật màn hình là đã kết nối thành công
            updateUi = new updateUI(update);
            // kiểm tra gọi những biến thread
            CheckForIllegalCrossThreadCalls = false;
        }

        // hàm khởi tạo kết nối
        private void starClient()
        {
            EndPoint ipep = new IPEndPoint(IPAddress.Parse(ipAddress.ToString()), Convert.ToInt32(port.ToString()));
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
          //  updateUi("Đã kết nối...");
            //// thực hiện việc kết nối và gọi beginConnect
            client.BeginConnect(ipep, new AsyncCallback(beginConnect), client); // ipep của thiết bị cần kết nối tới
            // đăng ký beginConnect khi có kết nối hoàn tất. truyển client đến EndConnect

        }

        // bắt đầu kết nối
        private void beginConnect(IAsyncResult ar)
        {
            try
            {
                client.EndConnect(ar);  // lấy socket của nơi gửi
                updateUi("Kết nối thành công tới Server: " + client.RemoteEndPoint.ToString());
                string welcome = "Hello Server";
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
                updateUi("Kết nối tới Server không thành công.");
                MessageBox.Show("Kết nối đến Server không thành công");
            }
        }

        // hàm hiển thị thông tin nhận được lên bảng chat

        private void update(string msg)
        {
            lstDisplay.Items.Add(msg);
            lstDisplay.TopIndex = lstDisplay.Items.Count - 1;
        }

        // gửi dữ liệu đến server
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

        // gửi lệnh đến server
        private void sendCommand(string data)
        {
            buffSend = new byte[1024];
            buffSend = Encoding.UTF8.GetBytes(data);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
        }

        
        

        // hàm nhận dữ liệu trả về từ server
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
                // đăng nhập thành công sẽ lấy tên người dùng
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DNTC")
                {
                    playerName = textBox1.Text;
                    //dashBoard();

                }
                
                // nếu thất bại cờ sẽ giữ nguyên : flag = 0 - sai thông tin người dung, flag = 1 - đúng
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DNTB")
                {
                    
                    
                    MessageBox.Show("Tên đăng nhập hoặc mật khẩu không đúng");
                    loginPage();
                }

                // nếu đăng nhập sai - server vẫn giữ tên đăng nhập. nhưng ko lưu vào danh sách đang online. đăng nhập đúng - sẽ mở dashboard
                if (receive.Length >= 9 && receive.Substring(0, 10) == "#_TCP_DNTT")
                {
                    //dashBoard();
                }

                // nhận dữ liệu trả về từ server. sau đó tách lấy những kí tự dưới đây.

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
               

                if (receive.Length >= 9 && receive.Substring(0, 9) == "#_Chat_00")
                {
                    updateUi(receive.Substring(9));
                }

                //cho phép nhận tiếp dữ liệu từ server
                s.BeginReceive(buffReceive, 0, buffReceive.Length, SocketFlags.None, new AsyncCallback(beginReceive), s);
            }
            catch { }
        }


        // biến toàn cục để lưu
        string tenDangNhap = "";
        string matKhau = "";
        string matKhauMoi = "";


        // Đăng nhập vào Dashboard -- Log In --
        private void button1_Click(object sender, EventArgs e)
        {
            
                // sau khi click vào log in - lấy dữ liệu vừa nhập vào và gửi đến server
            buffSend = new byte[1024];
            string str = "#_TCP_DN" + textBox1.Text + " " + textBox2.Text;
            tenDangNhap = textBox1.Text;
            matKhau = textBox2.Text;
            buffSend = Encoding.UTF8.GetBytes(str);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
            dashBoard();
            this.label1.Visible = false;
            this.label2.Visible = false;
            this.textBox1.Visible = false;
            this.textBox2.Visible = false;
            this.button1.Visible = false;
            this.button2.Visible = false;


                 // trường hợp đúng - sẽ mở dashboard -- nhớ ấn nút log in 2 lần 
                     

             // nếu sai - bắt đăng nhập lại


        }

        // Thoát khỏi tài khoản hiện tại để đăng nhập với tài khoản khác
        private void button11_Click(object sender, EventArgs e)
        {
            
            // giống đăng xuất -- mở lại form đăng nhập - và nick được xóa khỏi danh sách tài khoản đang online của server
            buffSend = new byte[1024];
            string str = "#_TCP_OUT";

            buffSend = Encoding.UTF8.GetBytes(str);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);



            loginPage();

            this.textBox1.Clear();
            this.textBox2.Clear();

        }

        private void loginPage()
        {
            this.textBox1.Visible = true;
            this.textBox2.Visible = true;
            this.label1.Visible = true;
            this.label2.Visible = true;
            this.button1.Visible = true;
            this.button2.Visible = true;


            this.button1a.Visible = false;
            this.button22.Visible = false;
            this.button3.Visible = false;
            this.button4.Visible = false;
            this.button5.Visible = false;
            this.button6.Visible = false;
            this.button7.Visible = false;
            this.button8.Visible = false;
            this.button9.Visible = false;
            this.button10.Visible = false;
            this.textBox3.Visible = false;
            this.button11.Visible = false;
            this.lstDisplay.Visible = false;
            this.textBox4.Visible = false;
            this.button12.Visible = false;



            // 
            // textBox1
            // 
            this.textBox1.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox1.Location = new System.Drawing.Point(222, 102);
            this.textBox1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(208, 31);
            this.textBox1.TabIndex = 0;

            // 
            // textBox2
            // 
            this.textBox2.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox2.Location = new System.Drawing.Point(222, 154);
            this.textBox2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBox2.Multiline = true;
            this.textBox2.Name = "textBox2";
            this.textBox2.PasswordChar = '*';
            this.textBox2.Size = new System.Drawing.Size(208, 31);
            this.textBox2.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(100, 105);
            this.label1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(78, 18);
            this.label1.TabIndex = 2;
            this.label1.Text = "Account";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(100, 154);
            this.label2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(95, 18);
            this.label2.TabIndex = 3;
            this.label2.Text = "Password";
            // 
            // button1
            // 
            this.button1.BackColor = System.Drawing.SystemColors.Info;
            this.button1.Font = new System.Drawing.Font("Verdana", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button1.Location = new System.Drawing.Point(329, 218);
            this.button1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(101, 32);
            this.button1.TabIndex = 4;
            this.button1.Text = "Log In";
            this.button1.UseVisualStyleBackColor = false;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.BackColor = System.Drawing.Color.DeepSkyBlue;
            this.button2.Font = new System.Drawing.Font("Verdana", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button2.Location = new System.Drawing.Point(222, 218);
            this.button2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(101, 32);
            this.button2.TabIndex = 5;
            this.button2.Text = "Sign Up";
            this.button2.UseVisualStyleBackColor = false;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.PaleTurquoise;
            this.ClientSize = new System.Drawing.Size(600, 395);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBox2);
            this.Controls.Add(this.textBox1);

            this.Name = "Form1";
            this.Text = "ClientSide";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        // Đăng kí tài khoản mới -- Sign Up --
        private void button2_Click(object sender, EventArgs e)
        {
            // tắt form đăng nhập - mở form đăng kí
            this.Hide();
            Form3 form3 = new Form3();
            form3.Show();
            
        }

        // Gửi tin nhắn đến server -- Send button --
        private void button10_Click(object sender, EventArgs e)
        {
            // chat 00 - là phòng chờ . chat 1 - trong phòng
            buffSend = new byte[1024];
            string str = "";
            if (inRoom == false)
            {
                str = "#_Chat_00" + textBox3.Text;
            }
            else
            {
                str = "#_Chat_1" + roomNumber.ToString() + textBox3.Text;
            }
            buffSend = Encoding.UTF8.GetBytes(str);
            client.BeginSend(buffSend, 0, buffSend.Length, SocketFlags.None, new AsyncCallback(sendData), client);
            textBox3.Clear();
            
        }
        // Mở form đổi mật khẩu
        private void button12_Click(object sender, EventArgs e) 
        {
            changePassword();
        }

        private void changePassword()
        {
            this.button1a.Visible = false;
            this.button22.Visible = false;
            this.button3.Visible = false;
            this.button4.Visible = false;
            this.button5.Visible = false;
            this.button6.Visible = false;
            this.button7.Visible = false;
            this.button8.Visible = false;
            this.button9.Visible = false;
            this.button10.Visible = false;
            this.textBox3.Visible = false;
            this.button11.Visible = false;
            this.lstDisplay.Visible = false;
            this.textBox4.Visible = false;
            this.button12.Visible = false;

            this.label5.Visible = true;
            this.label6.Visible = true;
            this.label7.Visible = true;
            this.textBox5.Visible = true;
            this.textBox6.Visible = true;
            this.textBox7.Visible = true;
            this.button15.Visible = true;
            this.button16.Visible = true;

            this.textBox5.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox5.Location = new System.Drawing.Point(210, 73);
            this.textBox5.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBox5.Multiline = true;
            this.textBox5.Name = "textBox5";
            this.textBox5.PasswordChar = '*';
            this.textBox5.Size = new System.Drawing.Size(241, 33);
            this.textBox5.TabIndex = 0;
            // 
            // textBox6
            // 
            this.textBox6.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox6.Location = new System.Drawing.Point(210, 140);
            this.textBox6.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBox6.Multiline = true;
            this.textBox6.Name = "textBox6";
            this.textBox6.PasswordChar = '*';
            this.textBox6.Size = new System.Drawing.Size(241, 33);
            this.textBox6.TabIndex = 1;
            // 
            // textBox7
            // 
            this.textBox7.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox7.Location = new System.Drawing.Point(210, 210);
            this.textBox7.ForeColor = System.Drawing.SystemColors.ControlText;
            this.textBox7.Multiline = true;
            this.textBox7.Name = "textBox7";
            this.textBox7.PasswordChar = '*';
            this.textBox7.Size = new System.Drawing.Size(241, 33);
            this.textBox7.TabIndex = 2;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(43, 73);
            this.label5.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(129, 18);
            this.label5.TabIndex = 3;
            this.label5.Text = "Old Password";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(43, 147);
            this.label6.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(140, 18);
            this.label6.TabIndex = 4;
            this.label6.Text = "New Password";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.Location = new System.Drawing.Point(43, 217);
            this.label7.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(127, 18);
            this.label7.TabIndex = 5;
            this.label7.Text = "Re-Password";
            // 
            // button15
            // 
            this.button15.BackColor = System.Drawing.Color.Orange;
            this.button15.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button15.Location = new System.Drawing.Point(329, 278);
            this.button15.Name = "button15";
            this.button15.Size = new System.Drawing.Size(122, 35);
            this.button15.TabIndex = 6;
            this.button15.Text = "Change";
            this.button15.UseVisualStyleBackColor = false;
           // this.button15.Click += new System.EventHandler(this.button15_Click);
            // 
            // button16
            // 
            this.button16.BackColor = System.Drawing.SystemColors.Highlight;
            this.button16.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button16.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.button16.Location = new System.Drawing.Point(210, 278);
            this.button16.Name = "button16";
            this.button16.Size = new System.Drawing.Size(113, 35);
            this.button16.TabIndex = 7;
            this.button16.Text = "Back";
            this.button16.UseVisualStyleBackColor = false;
            //this.button16.Click += new System.EventHandler(this.button16_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(539, 353);
            this.Controls.Add(this.button16);
            this.Controls.Add(this.button15);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.textBox7);
            this.Controls.Add(this.textBox6);
            this.Controls.Add(this.textBox5);
            this.Name = "Form1";
            this.Text = "ClientSide --Change Password--";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        // Form đổi mật khẩu
        private void button15_Click(object sender, EventArgs e)
        {

            if (textBox5.Text == "" || textBox6.Text == "" || textBox7.Text == "")
            {
                MessageBox.Show("Các trường dữ liệu không được để trống");
            }
            else
            {
                if (textBox5.Text != matKhau)
                {
                    MessageBox.Show("Mật khẩu cũ không đúng");
                }
                else
                {
                    if (textBox6.Text != textBox7.Text)
                    {
                        MessageBox.Show("Mật khẩu nhập lại không đúng");
                    }
                    else
                    {
                        sendCommand("#_TCP_DMK" + textBox7.Text);
                    }
                }
             }

            textBox5.Clear();
            textBox6.Clear();
            textBox7.Clear();
        }

        private void dashBoard()
        {
            this.textBox5.Visible = false;
            this.textBox6.Visible = false;
            this.textBox7.Visible = false;
            this.label5.Visible = false;
            this.label6.Visible = false;
            this.label7.Visible = false;
            this.button15.Visible = false;
            this.button16.Visible = false;




            this.button12.Visible = true;
            this.lstDisplay.Visible = true;
            this.button11.Visible = true;
            this.textBox3.Visible = true;
            this.button10.Visible = true;
            this.button9.Visible = true;
            this.button8.Visible = true;
            this.button7.Visible = true;
            this.button6.Visible = true;
            this.button5.Visible = true;
            this.button4.Visible = true;
            this.button3.Visible = true;
            this.button22.Visible = true;
            this.button1a.Visible = true;

            this.button1a.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button1a.Location = new System.Drawing.Point(32, 62);
            this.button1a.Name = "button1a";
            this.button1a.Size = new System.Drawing.Size(104, 59);
            this.button1a.TabIndex = 0;
            this.button1a.Text = "Room-1";
            this.button1a.UseVisualStyleBackColor = true;
            // 
            // button2
            // 
            this.button22.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button22.Location = new System.Drawing.Point(209, 62);
            this.button22.Name = "button22";
            this.button22.Size = new System.Drawing.Size(104, 59);
            this.button22.TabIndex = 1;
            this.button22.Text = "Room-2";
            this.button22.UseVisualStyleBackColor = true;
            // 
            // button3
            // 
            this.button3.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button3.Location = new System.Drawing.Point(389, 62);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(104, 59);
            this.button3.TabIndex = 2;
            this.button3.Text = "Room-3";
            this.button3.UseVisualStyleBackColor = true;
            // 
            // button4
            // 
            this.button4.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button4.Location = new System.Drawing.Point(32, 185);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(104, 59);
            this.button4.TabIndex = 3;
            this.button4.Text = "Room-4";
            this.button4.UseVisualStyleBackColor = true;
            // 
            // button5
            // 
            this.button5.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button5.Location = new System.Drawing.Point(209, 185);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(104, 59);
            this.button5.TabIndex = 4;
            this.button5.Text = "Room-5";
            this.button5.UseVisualStyleBackColor = true;
            // 
            // button6
            // 
            this.button6.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button6.Location = new System.Drawing.Point(389, 185);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(104, 59);
            this.button6.TabIndex = 5;
            this.button6.Text = "Room-6";
            this.button6.UseVisualStyleBackColor = true;
            // 
            // button7
            // 
            this.button7.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button7.Location = new System.Drawing.Point(32, 317);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(104, 59);
            this.button7.TabIndex = 6;
            this.button7.Text = "Room-7";
            this.button7.UseVisualStyleBackColor = true;
            // 
            // button8
            // 
            this.button8.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button8.Location = new System.Drawing.Point(209, 317);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(104, 59);
            this.button8.TabIndex = 7;
            this.button8.Text = "Room-8";
            this.button8.UseVisualStyleBackColor = true;
            // 
            // button9
            // 
            this.button9.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button9.Location = new System.Drawing.Point(389, 317);
            this.button9.Name = "button9";
            this.button9.Size = new System.Drawing.Size(104, 59);
            this.button9.TabIndex = 8;
            this.button9.Text = "Room-9";
            this.button9.UseVisualStyleBackColor = true;
            // 
            // button10
            // 
            this.button10.BackColor = System.Drawing.SystemColors.Info;
            this.button10.ForeColor = System.Drawing.Color.Maroon;
            this.button10.Location = new System.Drawing.Point(859, 366);
            this.button10.Name = "button10";
            this.button10.Size = new System.Drawing.Size(103, 36);
            this.button10.TabIndex = 9;
            this.button10.Text = "Send";
            this.button10.UseVisualStyleBackColor = false;
            //this.button10.Click += new System.EventHandler(this.button10_Click);
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(529, 366);
            this.textBox3.Multiline = true;
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(324, 36);
            this.textBox3.TabIndex = 10;
            //
            // button11
            // 
            this.button11.BackColor = System.Drawing.Color.DarkOrange;
            this.button11.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.button11.Location = new System.Drawing.Point(785, 12);
            this.button11.Name = "button11";
            this.button11.Size = new System.Drawing.Size(177, 41);
            this.button11.TabIndex = 12;
            this.button11.Text = "Back";
            this.button11.UseVisualStyleBackColor = false;
            this.button11.Click += new System.EventHandler(this.button11_Click);
            // 
            // lstDisplay
            // 
            this.lstDisplay.FormattingEnabled = true;
            this.lstDisplay.ItemHeight = 18;
            this.lstDisplay.Location = new System.Drawing.Point(529, 59);
            this.lstDisplay.Name = "lstDisplay";
            this.lstDisplay.Size = new System.Drawing.Size(433, 292);
            this.lstDisplay.TabIndex = 13;
            // 

            // button12
            // 
            this.button12.BackColor = System.Drawing.SystemColors.HotTrack;
            this.button12.Location = new System.Drawing.Point(589, 12);
            this.button12.Name = "button12";
            this.button12.Size = new System.Drawing.Size(175, 41);
            this.button12.TabIndex = 15;
            this.button12.Text = "Change Password";
            this.button12.UseVisualStyleBackColor = false;
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(10F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.ClientSize = new System.Drawing.Size(980, 408);
            
            this.Controls.Add(this.button12);

            this.Controls.Add(this.lstDisplay);
            this.Controls.Add(this.button11);
            this.Controls.Add(this.textBox3);
            this.Controls.Add(this.button10);
            this.Controls.Add(this.button9);
            this.Controls.Add(this.button8);
            this.Controls.Add(this.button7);
            this.Controls.Add(this.button6);
            this.Controls.Add(this.button5);
            this.Controls.Add(this.button4);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.button22);
            this.Controls.Add(this.button1a);
             
            this.Font = new System.Drawing.Font("Verdana", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.SystemColors.ControlLightLight;

            this.Margin = new System.Windows.Forms.Padding(5, 4, 5, 4);
            this.Name = "Form1";
            this.Text = "ClientSide -- DashBoard --";
            this.ResumeLayout(false);
            this.PerformLayout();
  
        }

        //nút Trở lại trong form đổi mật khẩu
        private void button16_Click(object sender, EventArgs e)
        {
            dashBoard();
        }


        private void button1a_Click(object sender, EventArgs e)
        {
            this.button12.Visible = false;
            this.lstDisplay.Visible = true;
            this.button11.Visible = false;
            this.textBox3.Visible = true;
            this.button10.Visible = true;
            this.button9.Visible = false;
            this.button8.Visible = false;
            this.button7.Visible = false;
            this.button6.Visible = false;
            this.button5.Visible = false;
            this.button4.Visible = false;
            this.button3.Visible = false;
            this.button22.Visible = false;
            this.button1a.Visible = false;

           

            this.button10.BackColor = System.Drawing.SystemColors.Info;
            this.button10.ForeColor = System.Drawing.Color.Maroon;
            this.button10.Location = new System.Drawing.Point(859, 366);
            this.button10.Name = "button10";
            this.button10.Size = new System.Drawing.Size(103, 36);
            this.button10.TabIndex = 9;
            this.button10.Text = "Send";
            this.button10.UseVisualStyleBackColor = false;
            //this.button10.Click += new System.EventHandler(this.button10_Click);

            this.textBox3.Location = new System.Drawing.Point(529, 366);
            this.textBox3.Multiline = true;
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(324, 36);
            this.textBox3.TabIndex = 10;

            this.lstDisplay.FormattingEnabled = true;
            this.lstDisplay.ItemHeight = 18;
            this.lstDisplay.Location = new System.Drawing.Point(529, 59);
            this.lstDisplay.Name = "lstDisplay";
            this.lstDisplay.Size = new System.Drawing.Size(433, 292);
            this.lstDisplay.TabIndex = 13;

            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 

            this.pictureBox1.Image = global::Client.Properties.Resources.chesspro;
            this.pictureBox1.Location = new System.Drawing.Point(21, 71);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(684, 487);
            this.pictureBox1.TabIndex = 0;
            this.pictureBox1.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(980, 487);
            this.Controls.Add(this.pictureBox1);
            this.Name = "Form1";
            this.Text = "Room-1";
            
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            

            inRoom = true;

            if (count <= 2)
            {
                roomNumber = 1;
                string _toServer = "#_TCP_IR" + roomNumber.ToString();
                sendCommand(_toServer);
                

            }
        }
        
    }
}