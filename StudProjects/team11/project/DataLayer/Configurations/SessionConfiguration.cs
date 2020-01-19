using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Model;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace DataLayer.Configurations
{
    class SessionConfiguration : IEntityTypeConfiguration<Session>
    {
        public void Configure(EntityTypeBuilder<Session> builder)
        {
            builder.HasKey(s => s.Id);

            builder.HasOne(s => s.App)
                .WithMany();

            builder.HasOne(s => s.Child)
                .WithMany();

            builder.Property(s => s.SessionData)
                .HasConversion(
                list => JsonConvert.SerializeObject(list), 
                json => JsonConvert.DeserializeObject<List<TimeEmotionPair>>(json));
        }
    }
}
