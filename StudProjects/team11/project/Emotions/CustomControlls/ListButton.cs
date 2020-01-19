using Prism.Commands;
using System;
using System.Windows.Input;

namespace Emotions.CustomControlls
{
    public class ListButton : ViewModelBase
    {
        public ListButton()
        {
            this.OnClick = new DelegateCommand(this.Click);
        }

        public ICommand OnClick { get; set; }


        private void Click()
        {
            this.Clicked?.Invoke(this, this);
        }

        public event EventHandler<ListButton> Clicked;
    }
}
