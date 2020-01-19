using BusinessLayer.Interfaces;
using Services;
using System;
using System.Windows;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using Emotions.Utils;
using System.Windows.Controls;
using System.Windows.Forms;
using MaterialDesignThemes.Wpf;

namespace Emotions
{
    /// <summary>
    /// Interaction logic for Login.xaml
    /// </summary>
    public partial class Login : System.Windows.Controls.UserControl
    {
        private BitmapImage faceScannerImage;

        ImageRecognitionService imageRecognitionService;

        public Login(ImageRecognitionService imageRecognitionService)
        {
            this.imageRecognitionService = imageRecognitionService;
            this.faceScannerImage = new BitmapImage(new Uri("/Images/faceScanner.jpg", UriKind.Relative));

            this.Unloaded += this.Login_Closing;
            this.Loaded += this.Login_Loaded;

            this.InitializeComponent();
        }

        private void Login_Loaded(object sender, RoutedEventArgs e)
        {
            this.imageRecognitionService.ImageReceived += this.FaceCutoutService_FaceFound;
        }

        private void Login_Closing(object sender, object e)
        {
            this.imageRecognitionService.ImageReceived -= this.FaceCutoutService_FaceFound;
        }

        private void FaceCutoutService_FaceFound(object sender, Face e)
        {
            System.Windows.Application.Current?.Dispatcher.InvokeAsync(() => { 
                if (e != null && e.Image !=null)
                {
                    this.detectedFaceImage.Source = e.Image.ToBitmapImage();
                }
                else
                {
                    this.detectedFaceImage.Source = this.faceScannerImage;
                }
            });
        }
    }
}
