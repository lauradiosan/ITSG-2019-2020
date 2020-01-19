using Microsoft.EntityFrameworkCore;
using Model;

namespace DataLayer.Configurations
{
    class AppConfiguration : IEntityTypeConfiguration<App>
    {
        public void Configure(Microsoft.EntityFrameworkCore.Metadata.Builders.EntityTypeBuilder<App> builder)
        {
            builder.HasKey(u => u.Id);
        }
    }
}
