using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using Emotions.Utils;
using MaterialDesignThemes.Wpf;
using Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Linq;
using System.Windows;

namespace Emotions.Windows.Children.ViewModels
{
    public class ApplicationsWindowViewModel : IDisposable
    {
        private IAppController appController;
        private IAuthenticationController authenticationController;
        private ImageRecognitionService imageRecognitionService;
        private Login login;
        private IEmotionRecordingController emotionRecordingController;
        private Process process;

        public ApplicationsWindowViewModel(IAppController appController, IAuthenticationController authenticationController, ImageRecognitionService imageRecognitionService, IEmotionRecordingController emotionRecordingController)
        {
            this.appController = appController;
            this.authenticationController = authenticationController;
            this.emotionRecordingController = emotionRecordingController;
            this.imageRecognitionService = imageRecognitionService;

            IEnumerable<ListItemViewModel> apps = appController.GetAllApplications().Select(app => {
                var vm = app.ToListItemViewModel();
                vm.Clicked += AppViewModel_Clicked;
                return vm;
            });

            this.login = new Login(imageRecognitionService);

            this.ApplicationPanelItems = new ObservableCollection<ListButton>(apps);
            authenticationController.ChildLoggedOut += this.AuthenticationController_ChildLoggedOut;
            authenticationController.ChildLoggedIn += this.AuthenticationController_ChildLoggedIn;
        }

        private void AuthenticationController_ChildLoggedIn(object sender, Model.Child e)
        {
            Application.Current.Dispatcher.InvokeAsync(() =>
            {
                DialogHost.CloseDialogCommand.Execute(null, this.login);
            });
        }

        private void AuthenticationController_ChildLoggedOut(object sender, Model.Child e)
        {
            Application.Current.Dispatcher.InvokeAsync(() =>
            {
                DialogHost.Show(this.login, "LoginDialogHost");

            if(process !=null && process.HasExited == false)
            {
                process.Kill();
            }
            });
        }

        public ObservableCollection<ListButton> ApplicationPanelItems { get; set; }

        private void AppViewModel_Clicked(object sender, ListButton e)
        {
            var app = (e as ApplicationListItem).ToApp();
            process = this.appController.StartApp(app);
            process.Exited += this.Process_Exited;
            this.emotionRecordingController.StartRecording(app, authenticationController.LoggedInChild);
        }

        private void Process_Exited(object sender, EventArgs e)
        {
            this.emotionRecordingController.StopRecording();
        }

        #region IDisposable Support
        private bool disposedValue = false; // To detect redundant calls

        protected virtual void Dispose(bool disposing)
        {
            if (!disposedValue)
            {
                if (disposing)
                {
                   // this.login.Close();
                }

                disposedValue = true;
            }
        }
        public void Dispose()
        {
            Dispose(true);
        }
        #endregion
    }
}
