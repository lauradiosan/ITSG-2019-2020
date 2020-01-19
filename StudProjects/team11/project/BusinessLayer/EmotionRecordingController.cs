using BusinessLayer.Interfaces;
using DataLayer;
using Microsoft.EntityFrameworkCore;
using Model;
using Services;
using System;
using System.Collections.Generic;
using System.Linq;

namespace BusinessLayer
{
    public class EmotionRecordingController : IEmotionRecordingController
    {
        ImageRecognitionService imageRecognitionService;

        App app;
        Child child;
        List<TimeEmotionPair> timeEmotionPairs;
        DateTime startDate;
        DateTime endDate;

        public EmotionRecordingController(ImageRecognitionService imageRecognitionService)
        {
            this.imageRecognitionService = imageRecognitionService;
            this.timeEmotionPairs = new List<TimeEmotionPair>();
        }

        public List<Session> GetAllSessions()
        {
             using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                return applicationDbContext.Sessions.Include(s => s.Child).Include(s => s.App).ToList();
            }
        }

        public void StartRecording(App app, Child child)
        {
            this.app = app;
            this.child = child;
            this.startDate = DateTime.Now;
            this.imageRecognitionService.ImageReceived += this.ImageRecognitionService_ImageReceived;
        }

        private void ImageRecognitionService_ImageReceived(object sender, Face e)
        {
            if (e.Image != null)
            {
                this.timeEmotionPairs.Add(new TimeEmotionPair()
                {
                    RecordedAt = DateTime.Now,
                    Emotion = (Emotion)e.Emotion
                });
            }
        }

        public void StopRecording()
        {
            this.imageRecognitionService.ImageReceived -= this.ImageRecognitionService_ImageReceived;
            this.endDate = DateTime.Now;

            using (ApplicationDbContext applicationDbContext = new ApplicationDbContext())
            {
                applicationDbContext.Attach(child);
                applicationDbContext.Attach(app);
                applicationDbContext.Add(new Session()
                {
                    Child = child,
                    App = app,
                    SessionData = timeEmotionPairs,
                    SessionStart = startDate,
                    SessionEnd = endDate
                });
                applicationDbContext.SaveChanges();
            }

            this.timeEmotionPairs.Clear();
            this.app = null;
            this.child = null;
        }
    }
}
