using BusinessLayer.Interfaces;
using Emotions.CustomControlls;
using Emotions.Utils;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace Emotions.Windows.Management.ViewModels
{
    public class ApplicationsPageViewModel
    {
        private IAppController appController;
        private ListButton addButton;

        public ApplicationsPageViewModel(IAppController appController)
        {
            this.appController = appController;

            this.addButton = new ListButton();
            this.addButton.Clicked += this.ApplicationAddItem_Clicked;

            IEnumerable<ListItemViewModel> apps = appController.GetAllApplications().Select(app => {
                var vm = app.ToListItemViewModel();
                vm.Clicked += this.AppViewModel_Clicked;
                vm.Deleted += this.AppViewModel_Deleted;
                return vm;
            });

            this.ApplicationPanelItems = new ObservableCollection<ListButton>(apps);
            this.ApplicationPanelItems.Add(this.addButton);
        }

        public ObservableCollection<ListButton> ApplicationPanelItems { get; set; }

        private void ApplicationAddItem_Clicked(object sender, ListButton e)
        {
            OpenFileDialog opf = new OpenFileDialog();
            opf.Multiselect = false;
            opf.Filter = "Executable (*.exe)|*.exe";
            opf.Title = "Open an application";
            DialogResult result = opf.ShowDialog();

            if (result == DialogResult.OK)
            {
                Model.App app = new Model.App()
                {
                    Name = Path.GetFileNameWithoutExtension(opf.FileName),
                    Path = opf.FileName
                };
                this.appController.AddApp(app);

                ListItemViewModel appViewModel = app.ToListItemViewModel();

                appViewModel.Deleted += this.AppViewModel_Deleted;
                appViewModel.Clicked += this.AppViewModel_Clicked;

                this.ApplicationPanelItems.Remove(this.addButton);
                this.ApplicationPanelItems.Add(appViewModel);
                this.ApplicationPanelItems.Add(this.addButton);
            }
        }

        private void AppViewModel_Clicked(object sender, ListButton e)
        {
            var app = e as ApplicationListItem;
            this.appController.StartApp(new Model.App() { Id = app.Id, Path = app.Path, Name = app.Name });
        }

        private void AppViewModel_Deleted(object sender, ListItemViewModel e)
        {
            var app = e as ApplicationListItem;
            this.appController.RemoveApp(app.ToApp());
            this.ApplicationPanelItems.Remove(e);
        }
    }
}
