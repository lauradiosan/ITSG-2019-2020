using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using LiveCharts;

using LiveCharts.Configurations;
using LiveCharts.Wpf;
using Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Emotions.Utils;

namespace Emotions.Windows.Management.ViewModels
{
    public class SessionDataPageViewModel : ViewModelBase
    {
        Brush[] brushes = new[]
            {
                Brushes.Red,
                Brushes.Green,
                Brushes.Gray,
                Brushes.Orange,
                Brushes.Blue,
                Brushes.Yellow,
                Brushes.Black
            };
        private SeriesCollection series;
        private SeriesCollection pie;
        private List<Session> sessions;
        private Session selectedSession;
        private IChildrenController childrenController;
        private IEmotionRecordingController emotionRecordingController;
        private BitmapImage picture;

        public SessionDataPageViewModel(IEmotionRecordingController emotionRecordingController, IChildrenController childrenController)
        {
            this.childrenController = childrenController;
            this.emotionRecordingController = emotionRecordingController;
            CartesianMapper<TimeEmotionPair> dayConfig = Mappers.Xy<TimeEmotionPair>()
                 .X(dayModel => (double)dayModel.RecordedAt.Ticks / TimeSpan.FromHours(1).Ticks)
                 .Y(dayModel => 5)
                 .Stroke(da => Brushes.Transparent)
                 .Fill(da => brushes[(int)da.Emotion]);
            Series = new SeriesCollection(dayConfig);
            Formatter = value => new System.DateTime((long)((value>0? value : 0) * TimeSpan.FromHours(1).Ticks)).ToString("t");

            this.Pie = new SeriesCollection();

            PointLabel = chartPoint => chartPoint.Participation > 0 ?
               string.Format("{0} ({1:P})", chartPoint.SeriesView.Title, chartPoint.Participation): string.Empty;

            this.Loaded();
        }

        public void Loaded()
        {
            this.Sessions = this.emotionRecordingController.GetAllSessions();

            this.SelectedSession = this.Sessions.FirstOrDefault();
        }

        public Func<double, string> Formatter { get; set; }

        public BitmapImage Picture
        {
            get => picture;
            set
            {
                picture = value;
                this.NotifyPropertyChange();
            }
        }

        public SeriesCollection Series
        {
            get => series;
            set
            {
                series = value;
                this.NotifyPropertyChange();
            }
        }

        public SeriesCollection Pie
        {
            get => pie;
            set
            {
                pie = value;
                this.NotifyPropertyChange();
            }
        }

        public List<Session> Sessions
        {
            get => sessions;
            set
            {
                sessions = value;
                this.NotifyPropertyChange();
            }
        }
        public Session SelectedSession
        {
            get => selectedSession;
            set
            {
                selectedSession = value;
                this.NotifyPropertyChange();
                if (value != null)
                { PrepareSeries(); }
            }
        }

        private void PrepareSeries()
        {
            this.Series.Clear();
            this.Series.Add(
            new LineSeries
            {
                Values = new ChartValues<TimeEmotionPair>(selectedSession.SessionData),
                Fill = Brushes.Transparent,
                PointGeometrySize = 15
            });

            TimeSpan[] durations = new TimeSpan[7];
            var current = selectedSession.SessionData[0];
            for (int i = 0; i < selectedSession.SessionData.Count; i++)
            {
                var pair = selectedSession.SessionData[i];
                if (current.Emotion != pair.Emotion || i + 1 == selectedSession.SessionData.Count)
                {
                    if (durations[(int)current.Emotion] == null)
                    {
                        durations[(int)current.Emotion] = new TimeSpan();
                    }
                    durations[(int)current.Emotion] += (pair.RecordedAt - current.RecordedAt);
                    current = pair;
                }
            }
            var mapping = durations.Select((a, b) =>
            {
                return new PieSeries()
                {
                    LabelPoint = PointLabel,
                    DataLabels = true,
                    Values = new ChartValues<double>() { a.Seconds },
                    Title = ((Emotion)b).ToString(),
                    Fill = brushes[b]
                };
            }).ToList();
            this.Pie.Clear();
            this.Pie.AddRange(mapping);

            this.Picture = childrenController.LoadImage(selectedSession.Child.ImageId).ToBitmapImage();
        }

        public Func<ChartPoint, string> PointLabel { get; set; }
    }
}
