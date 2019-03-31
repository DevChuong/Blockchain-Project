using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Server
{
    public class Room
    {
        int giaTriXNTruoc;

        public int GiaTriXNTruoc
        {
            get { return giaTriXNTruoc; }
            set { giaTriXNTruoc = value; }
        }
        List<User> listPlayer = new List<User>();

        public List<User> ListPlayer
        {
            get { return listPlayer; }
            set { listPlayer = value; }
        }
        int roomNumber;

        public int RoomNumber
        {
            get { return roomNumber; }
            set { roomNumber = value; }
        }

        public Room(int ma)
        {
            this.roomNumber = ma;
            this.giaTriXNTruoc = 0;
        }

        public bool addPlayer(User us)
        {
            if(listPlayer.Count <= 2)
            {
                listPlayer.Add(us);
                return true;
            }
            return false;
        }

        public bool removePlayer(User us, string userName)
        {
            if(listPlayer.Count() > 0)
            {
                for(int i = 0; i < listPlayer.Count(); i++)
                {
                    if(userName == listPlayer[i].UserName)
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
    }
}
