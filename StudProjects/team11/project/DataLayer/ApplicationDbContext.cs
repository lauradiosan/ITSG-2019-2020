using Microsoft.EntityFrameworkCore;
using Model;
using System.Reflection;

namespace DataLayer
{
    public class ApplicationDbContext : DbContext
    {
        public DbSet<Child> Children { get; set; }
        public DbSet<App> Apps { get; set; }
        public DbSet<Session> Sessions { get; set; }
        
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlServer(@"Server=localhost\SQLEXPRESS;Database=Emotions;Trusted_Connection=True;");
            base.OnConfiguring(optionsBuilder);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
            base.OnModelCreating(modelBuilder);
        }
    }
}
