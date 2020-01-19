using System;

namespace Model
{
    public class TimeEmotionPair
    {
        public DateTime RecordedAt { get; set; }
        public Emotion Emotion { get; set; }
    }
}
