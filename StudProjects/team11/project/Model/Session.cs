using System;
using System.Collections.Generic;

namespace Model
{
    public class Session
    {
        public int Id { get; set; }
        public DateTime SessionStart { get; set; }
        public DateTime SessionEnd { get; set; }
        public List<TimeEmotionPair> SessionData { get; set; }

        public int ChildId { get; set; }
        public Child Child { get; set; }

        public int AppId { get; set; }
        public App App { get; set; }
    }
}
