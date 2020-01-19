using BusinessLayer;
using BusinessLayer.Interfaces;
using Emotions.Windows.Management.ViewModels;
using LiveCharts;
using LiveCharts.Configurations;
using LiveCharts.Wpf;
using Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Emotions.Windows.Management
{
    /// <summary>
    /// Interaction logic for SessionDataPage.xaml
    /// </summary>
    public partial class SessionDataPage : UserControl
    {
        /*public enum Emotion
            {
                Angry,
                Disgust,
                Fear,
                Happy,
                Sad,
                Surprise,
                Neutral
            }*/
        
        public SessionDataPage(IEmotionRecordingController emotionRecordingController, IChildrenController childrenController)
        {
            InitializeComponent();

            DataContext = new SessionDataPageViewModel(emotionRecordingController, childrenController);
            this.Loaded += this.SessionDataPage_Loaded;
        }

        private void SessionDataPage_Loaded(object sender, RoutedEventArgs e)
        {
            ((SessionDataPageViewModel)this.DataContext).Loaded();
        }
    }
}
