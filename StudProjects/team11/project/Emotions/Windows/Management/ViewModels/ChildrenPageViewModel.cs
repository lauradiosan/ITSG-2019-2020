using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using Services;
using System;
using System.Collections.Generic;
using System.Linq;
using Emotions.Utils;
using System.Collections.ObjectModel;
using MaterialDesignThemes.Wpf;
using Model;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using Emotions.Utils;
using System.Drawing;

namespace Emotions.Windows.Management
{
    public class ChildrenPageViewModel : ViewModelBase
    {
        private IChildrenController childrenController;
        private ImageRecognitionService imageRecognitionService;
        private ListButton addButton;

        public ChildrenPageViewModel(IChildrenController childrenController, ImageRecognitionService imageRecognitionService)
        {
            this.childrenController = childrenController;
            this.imageRecognitionService = imageRecognitionService;

            this.addButton = new ListButton();
            this.addButton.Clicked += this.ApplicationAddItem_Clicked;

            IEnumerable<ListItemViewModel> apps = childrenController.GetAllChildren().Select(child =>
            {
                var vm = child.ToListItemViewModel();
                vm.Icon = childrenController.LoadImage(child.ImageId).ToBitmapImage();
                vm.Deleted += this.Vm_Deleted;
                return vm;
            });

            this.ApplicationPanelItems = new ObservableCollection<ListButton>(apps);
            this.ApplicationPanelItems.Add(this.addButton);
        }

        private void Vm_Deleted(object sender, ListItemViewModel e)
        {
            var child = e as ChildListItem;
            this.childrenController.RemoveChild(child.Id);
            this.ApplicationPanelItems.Remove(e);
        }

        public ObservableCollection<ListButton> ApplicationPanelItems { get; set; }

        private void ApplicationAddItem_Clicked(object sender, ListButton e)
        {
            DialogHost.Show(new AddChildDialog(this.imageRecognitionService)).ContinueWith((res) =>
            {
                (Child, Bitmap) pair = ((Child, Bitmap))res.Result;

                this.childrenController.AddChild(pair.Item1, pair.Item2);

                var vm = pair.Item1.ToListItemViewModel();
                vm.Deleted += this.AppViewModel_Deleted;
                vm.Icon = pair.Item2.ToBitmapImage();
                this.ApplicationPanelItems.Remove(this.addButton);
                this.ApplicationPanelItems.Add(vm);
                this.ApplicationPanelItems.Add(this.addButton);
            }, TaskScheduler.FromCurrentSynchronizationContext());
        }

        private void AppViewModel_Deleted(object sender, ListItemViewModel e)
        {
            var child = e as ChildListItem;
            this.childrenController.RemoveChild(child.Id);
            this.ApplicationPanelItems.Remove(e);
        }

    }
}
