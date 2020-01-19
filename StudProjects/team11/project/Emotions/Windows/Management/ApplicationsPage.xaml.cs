using BusinessLayer.Interfaces;
using Emotions.Windows.Management.ViewModels;

namespace Emotions.Windows.Management
{
    /// <summary>
    /// Interaction logic for ApplicationsPage.xaml
    /// </summary>
    public partial class ApplicationsPage : System.Windows.Controls.UserControl
    {
        public ApplicationsPage(IAppController appController)
        {
            this.InitializeComponent();

            this.DataContext = new ApplicationsPageViewModel(appController);
        }
    }
}
