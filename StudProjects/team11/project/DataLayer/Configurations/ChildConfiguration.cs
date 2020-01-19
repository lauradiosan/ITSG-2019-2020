using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Model;
using Newtonsoft.Json;

namespace DataLayer.Configurations
{
    class ChildConfiguration : IEntityTypeConfiguration<Child>
    {
        public void Configure(EntityTypeBuilder<Child> builder)
        {
            builder.Property(u => u.Yhat)
                .HasConversion(
                 arr => JsonConvert.SerializeObject(arr),
                 json => JsonConvert.DeserializeObject<double[]>(json)
                );
            
            builder.HasKey(u => u.Id);
        }
    }
}
