using BusinessLayer.Interfaces;
using Model;
using Emotions.Utils;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Pen = System.Windows.Media.Pen;
using Services;

namespace Emotions
{
    /// <summary>
    /// Interaction logic for Login.xaml
    /// </summary>
    public partial class Debug : Window
    {
        ImageRecognitionService imageRecognitionService;

        public Debug(ImageRecognitionService imageRecognitionService)
        {
            this.imageRecognitionService = imageRecognitionService;

            this.InitializeComponent();

            this.Closing += this.Debug_Closing;

            this.imageRecognitionService.ImageReceived += this.ImageRecognitionService_ImageReceived;
        }

        private void ImageRecognitionService_ImageReceived(object sender, Face face)
        {
            Application.Current?.Dispatcher.InvokeAsync(() =>
            {
                if (face != null)
                {
                    if (face.Emotion != null)
                    {
                        this.emotion.Text =((Emotion)face.Emotion).ToString();
                    }
                    if (face.Image != null)
                    {
                        this.originalVideoFrameHolder.Source = face.Image.ToBitmapImage();
                    }
                }
            });
        }

        private void Debug_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            this.imageRecognitionService.ImageReceived -= this.ImageRecognitionService_ImageReceived;
        }
        /*
        private void IdentityController_UserLoggedOut(object sender, Child e)
        {
            Application.Current?.Dispatcher.InvokeAsync(() =>
            {
                if (e != null)
                {
                    this.loggedInUser.Text = "None";
                    this.lastUserAction.Text = "Logout";
                }
            });
        }

        private void IdentityController_UserLoggedIn(object sender, Child e)
        {
            Application.Current?.Dispatcher.InvokeAsync(() =>
            {
                if (e != null)
                {
                    this.loggedInUser.Text = e.UserName;
                    this.lastUserAction.Text = "Login";
                }
            });
        }



        private void UserHandler(object sender, Model.Child e)
        {
            Application.Current?.Dispatcher.InvokeAsync(() =>
            {
                if (e != null)
                {
                    this.visibleUser.Text = e.UserName;
                }
            });
        }
        
        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Child user = this.identityController.VisibleUser;
            if (user != null && user.Id == 0)
            {
                user.UserName = this.registerFaceName.Text;
                this.identityController.AddUser(user);
            }
        }
        */

    }  
}
