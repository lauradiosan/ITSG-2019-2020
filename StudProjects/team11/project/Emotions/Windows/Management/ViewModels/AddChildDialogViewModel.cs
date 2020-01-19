using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using MaterialDesignThemes.Wpf;
using Model;
using Prism.Commands;
using Services;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media.Imaging;

namespace Emotions.Windows.Management.ViewModels
{
    public class AddChildDialogViewModel:ViewModelBase
    {
        ImageRecognitionService imageRecognitionService;

        private string userName;
        private BitmapImage childImage;
        private Bitmap image;
        private double[] yhat;

        public AddChildDialogViewModel(ImageRecognitionService imageRecognitionService)
        {
            this.imageRecognitionService = imageRecognitionService;
            this.imageRecognitionService.ImageReceived += this.ImageRecognitionService_ImageReceived;

            this.SaveCommand = new DelegateCommand<IInputElement>(this.Save, (o)=> this.ChildImage != null && this.UserName !=null).ObservesProperty(() => this.ChildImage).ObservesProperty(()=> this.UserName);
            this.CaptureFrameCommand = new DelegateCommand(this.CaptureFrame, () => this.ChildImage != null).ObservesProperty(() => this.ChildImage);
        }

        public BitmapImage ChildImage 
        { 
            get => this.childImage;
            set 
            {
                this.childImage = value;
                this.NotifyPropertyChange();
            }
        }

        public string UserName 
        { 
            get => this.userName;
            set => this.SetProperty(ref this.userName, value);
        }

        public (Child, Bitmap) Result
        {
            get
            {
                Child child = new Model.Child()
                {
                    UserName = this.userName,
                    Yhat = this.yhat,
                };

                return (child, this.image);
            }
        }

        public ICommand SaveCommand { get; set; }
        public ICommand CaptureFrameCommand { get; set; }
    
        private void ImageRecognitionService_ImageReceived(object sender, Face e)
        {
            this.yhat = e.Yhat;
            Application.Current.Dispatcher.InvokeAsync(() =>
            {
                if (e.Image != null) {
                    this.image = e.Image;
                    this.ChildImage = Utils.Utils.ToBitmapImage(e.Image);
                }
            });
        }

        private void Save(IInputElement element)
        {
            DialogHost.CloseDialogCommand?.Execute(this.Result, element);
        }

        private void CaptureFrame()
        {
            this.imageRecognitionService.ImageReceived -= this.ImageRecognitionService_ImageReceived;
        }
    }
}
