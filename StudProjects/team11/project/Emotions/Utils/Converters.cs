using Emotions.CustomControlls;

namespace Emotions.Utils
{
    public static class Converters
    {
        public static Model.App ToApp(this ApplicationListItem appViewModel)
        {
            return new Model.App()
            {
                Id = appViewModel.Id,
                Name = appViewModel.Name,
                Path = appViewModel.Path
            };
        }

        public static ApplicationListItem ToListItemViewModel(this Model.App app)
        {
            return new ApplicationListItem
            {
                Id = app.Id,
                Name = app.Name,
                Path = app.Path
            };
        }

        public static Model.Child ToChild(this ChildListItem appViewModel)
        {
            return new Model.Child()
            {
                Id = appViewModel.Id,
                UserName = appViewModel.Name
            };
        }

        public static ChildListItem ToListItemViewModel(this Model.Child app)
        {
            return new ChildListItem
            {
                Id = app.Id,
                Name = app.UserName
            };
        }
    }
}
