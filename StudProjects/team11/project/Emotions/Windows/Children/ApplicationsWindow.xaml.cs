using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using Emotions.Windows.Children.ViewModels;
using Services;

namespace Emotions.Windows.Children
{
    /// <summary>
    /// Interaction logic for ApplicationsWindow.xaml
    /// </summary>
    public partial class ApplicationsWindow : Window
    {
        IAuthenticationController authenticationController;
        public ApplicationsWindow(IAppController appController, IAuthenticationController authenticationController, ImageRecognitionService imageRecognitionService, IEmotionRecordingController emotionRecordingController)
        {
            this.InitializeComponent();

            this.DataContext = new ApplicationsWindowViewModel(appController, authenticationController, imageRecognitionService, emotionRecordingController);
            this.ContentRendered += (object a, EventArgs b) =>
            {
                authenticationController.ForceLogout();
            };
        }
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            (this.DataContext as ApplicationsWindowViewModel).Dispose();
            this.Close();
        }

    }
}
