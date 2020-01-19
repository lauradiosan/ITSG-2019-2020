using BusinessLayer;
using BusinessLayer.Interfaces;
using Emotions.Windows.Children;
using Grpc.Core;
using Services;
using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows;
using System.Windows.Forms;

namespace Emotions
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : System.Windows.Application
    {
        ImageRecognitionService imageRecognitionService;
        AuthenticationController authenticationController;
        ChildrenController childrenController;
        AppController appController;
        EmotionRecordingController emotionRecordingController;

        ManagementWindow managementWindow;

        Channel channel;
        Server server;

        public App()
        {
            this.Startup += this.App_Startup;
        }

        private void App_Startup(object sender, StartupEventArgs e)
        {
            this.Bootstrap();
            this.managementWindow = new ManagementWindow(this.imageRecognitionService, this.appController, this.childrenController, emotionRecordingController);
            this.managementWindow.StartChildrenApp += this.ManagementWindow_StartChildrenApp;
            this.managementWindow.Show();
        }

        private void ManagementWindow_StartChildrenApp(object sender, EventArgs e)
        {
            this.managementWindow.Hide();
            ApplicationsWindow applicationsWindow = new ApplicationsWindow(this.appController, this.authenticationController, this.imageRecognitionService, emotionRecordingController);
            applicationsWindow.Closing += this.ApplicationsWindow_Closing;
            applicationsWindow.Show();
        }

        private void ApplicationsWindow_Closing(object sender, CancelEventArgs e)
        {
            this.managementWindow.Show();
        }

        private void Bootstrap()
         {
            this.imageRecognitionService = new ImageRecognitionService();
            this.server = new Server
            {
                Services = { FaceDetection.BindService(this.imageRecognitionService) },
                Ports = { new ServerPort("localhost", 50001, ServerCredentials.Insecure) }
            };
            this.server.Start();

            this.appController = new AppController();
            this.childrenController = new ChildrenController();
            this.authenticationController = new AuthenticationController(this.childrenController, this.imageRecognitionService, 5000, 5000);
            this.emotionRecordingController = new EmotionRecordingController(this.imageRecognitionService);

            this.Exit += this.App_Exit;
            this.CreateNotifyicon();
         }

         private void App_Exit(object sender, ExitEventArgs e)
         {
             this.channel.ShutdownAsync().Wait();
         }

         private void CreateNotifyicon()
         {
             IContainer components = new Container();

             MenuItem exitButton = new MenuItem();
             exitButton.Index = 0;
             exitButton.Text = "Exit";
             exitButton.Click += this.exitButton_Click;

             MenuItem debugButton = new MenuItem();
             debugButton.Index = 1;
             debugButton.Text = "Debug";
             debugButton.Click += this.debugButton_Click;

             ContextMenu contextMenu = new ContextMenu();
             contextMenu.MenuItems.AddRange(
                         new MenuItem[] { exitButton, debugButton });


             NotifyIcon notifyIcon = new NotifyIcon(components);

             notifyIcon.Icon = Icon.FromHandle(SystemIcons.Application.Handle);

             notifyIcon.ContextMenu = contextMenu;

             notifyIcon.Text = "Emotion Tracker";
             notifyIcon.Visible = true;
         }

         private void exitButton_Click(object Sender, EventArgs e)
         {
             this.Shutdown();
         }

         private void debugButton_Click(object Sender, EventArgs e)
         {
             Debug debugWindow = new Debug(this.imageRecognitionService);
             debugWindow.Show();
         }
    }
}
