using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Server
{
    public class UserList
    {
        List<User> listPlayer = new List<User>();

        public List<User> ListPlayer
        {
            get { return listPlayer; }
            set { listPlayer = value; }
        }

        public bool addPlayer(User us)
        {
            if (listPlayer.Count <= 2)
            {
                listPlayer.Add(us);
                return true;
            }
            return false;
        }

        public bool removePlayer(User us, string userName)
        {
            if (listPlayer.Count() > 0)
            {
                for (int i = 0; i < listPlayer.Count(); i++)
                {
                    if (userName == listPlayer[i].UserName)
                    {
                        listPlayer.RemoveAt(i);
                        return true;
                    }
                }
            }
            return false;
        }

        public int playerCount()
        {
            return listPlayer.Count();
        }

        public string searchPlayer(Socket s)
        {
            if(listPlayer.Count > 0)
            {
                for(int i = 0; i < listPlayer.Count(); i++)
                {
                    if(listPlayer[i]._Socket.RemoteEndPoint.ToString() == s.RemoteEndPoint.ToString())
                    {
                        return listPlayer[i].UserName;
                    }
                }
            }
            return null;
        }
    }
}
