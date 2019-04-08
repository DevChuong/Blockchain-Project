namespace Server
{
    partial class frmServer
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmServer));
            this.btnStart = new System.Windows.Forms.Button();
            this.btnClose = new System.Windows.Forms.Button();
            this.lstDisplay = new System.Windows.Forms.ListBox();
            this.txtSend = new System.Windows.Forms.TextBox();
            this.btnSend = new System.Windows.Forms.Button();
            this.lsvListPlayer = new System.Windows.Forms.ListView();
            this.label1 = new System.Windows.Forms.Label();
            this.lblNguoiNhan = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.timer2 = new System.Windows.Forms.Timer(this.components);
            this.SuspendLayout();
            // 
            // btnStart
            // 
            this.btnStart.BackColor = System.Drawing.Color.Lime;
            this.btnStart.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnStart.Location = new System.Drawing.Point(577, 343);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(136, 44);
            this.btnStart.TabIndex = 0;
            this.btnStart.Text = "Start Server";
            this.btnStart.UseVisualStyleBackColor = false;
            this.btnStart.Click += new System.EventHandler(this.btnStart_Click);
            // 
            // btnClose
            // 
            this.btnClose.BackColor = System.Drawing.Color.Red;
            this.btnClose.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnClose.Font = new System.Drawing.Font("Verdana", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnClose.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnClose.Location = new System.Drawing.Point(20, 343);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(147, 44);
            this.btnClose.TabIndex = 3;
            this.btnClose.Text = "Close Server";
            this.btnClose.UseVisualStyleBackColor = false;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // lstDisplay
            // 
            this.lstDisplay.Font = new System.Drawing.Font("Verdana", 9F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Italic))), System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lstDisplay.FormattingEnabled = true;
            this.lstDisplay.ItemHeight = 14;
            this.lstDisplay.Location = new System.Drawing.Point(12, 22);
            this.lstDisplay.Name = "lstDisplay";
            this.lstDisplay.Size = new System.Drawing.Size(373, 270);
            this.lstDisplay.TabIndex = 4;
            // 
            // txtSend
            // 
            this.txtSend.Location = new System.Drawing.Point(215, 349);
            this.txtSend.Multiline = true;
            this.txtSend.Name = "txtSend";
            this.txtSend.Size = new System.Drawing.Size(214, 31);
            this.txtSend.TabIndex = 1;
            // 
            // btnSend
            // 
            this.btnSend.BackColor = System.Drawing.SystemColors.GradientInactiveCaption;
            this.btnSend.Font = new System.Drawing.Font("Verdana", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnSend.Location = new System.Drawing.Point(447, 349);
            this.btnSend.Name = "btnSend";
            this.btnSend.Size = new System.Drawing.Size(75, 31);
            this.btnSend.TabIndex = 2;
            this.btnSend.Text = "Send";
            this.btnSend.UseVisualStyleBackColor = false;
            this.btnSend.Click += new System.EventHandler(this.btnSend_Click);
            // 
            // lsvListPlayer
            // 
            this.lsvListPlayer.Font = new System.Drawing.Font("Verdana", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lsvListPlayer.FullRowSelect = true;
            this.lsvListPlayer.GridLines = true;
            this.lsvListPlayer.Location = new System.Drawing.Point(403, 22);
            this.lsvListPlayer.Name = "lsvListPlayer";
            this.lsvListPlayer.Size = new System.Drawing.Size(355, 270);
            this.lsvListPlayer.TabIndex = 5;
            this.lsvListPlayer.UseCompatibleStateImageBehavior = false;
            this.lsvListPlayer.View = System.Windows.Forms.View.Details;
            this.lsvListPlayer.ItemSelectionChanged += new System.Windows.Forms.ListViewItemSelectionChangedEventHandler(this.lsvListPlayer_ItemSelectionChanged);
            this.lsvListPlayer.SelectedIndexChanged += new System.EventHandler(this.lsvListPlayer_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Verdana", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(212, 315);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(130, 16);
            this.label1.TabIndex = 6;
            this.label1.Text = "Message To User";
            // 
            // lblNguoiNhan
            // 
            this.lblNguoiNhan.AutoSize = true;
            this.lblNguoiNhan.Font = new System.Drawing.Font("Verdana", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblNguoiNhan.Location = new System.Drawing.Point(355, 315);
            this.lblNguoiNhan.Name = "lblNguoiNhan";
            this.lblNguoiNhan.Size = new System.Drawing.Size(0, 16);
            this.lblNguoiNhan.TabIndex = 6;
            // 
            // timer1
            // 
            this.timer1.Interval = 5000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // timer2
            // 
            this.timer2.Interval = 3000;
            this.timer2.Tick += new System.EventHandler(this.timer2_Tick);
            // 
            // frmServer
            // 
            this.AcceptButton = this.btnSend;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.CancelButton = this.btnClose;
            this.ClientSize = new System.Drawing.Size(770, 406);
            this.Controls.Add(this.lblNguoiNhan);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.lsvListPlayer);
            this.Controls.Add(this.btnSend);
            this.Controls.Add(this.txtSend);
            this.Controls.Add(this.lstDisplay);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.btnStart);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "frmServer";
            this.Text = "Server";
            this.Load += new System.EventHandler(this.frmServer_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.ListBox lstDisplay;
        private System.Windows.Forms.TextBox txtSend;
        private System.Windows.Forms.Button btnSend;
        private System.Windows.Forms.ListView lsvListPlayer;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lblNguoiNhan;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Timer timer2;
    }
}

