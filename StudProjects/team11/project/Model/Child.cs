using System;
using System.ComponentModel.DataAnnotations.Schema;

namespace Model
{
    public class Child
    {
        public int Id { get; set; }

        public string UserName { get; set; }

        public string ImageId { get; set; }

        public double[] Yhat { get; set; }
    }
}
