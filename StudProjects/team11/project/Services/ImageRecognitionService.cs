using System;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Google.Protobuf.WellKnownTypes;
using Grpc.Core;

namespace Services
{
    public class ImageRecognitionService : FaceDetection.FaceDetectionBase
    {
        public override Task<Empty> SendProcessedData(ImageData request, ServerCallContext context)
        {
            return Task.Run(()=>
            {
                if (request != null)
                {
                    Face face = new Face();
                    if(request.Embedding != null && request.Embedding.Count>0)
                    {
                        face.Yhat = request.Embedding.ToArray();
                    }

                    if (request.Emotion != null)
                    {
                        face.Emotion = request.Emotion;
                    }

                    if(request.ImageBytes != null && request.ImageBytes.Length >0)
                    {
                        face.Image = new Bitmap(new MemoryStream(request.ImageBytes.ToArray()));
                    }

                    this.ImageReceived?.Invoke(this, face);
                }
                else
                {
                    this.ImageReceived?.Invoke(this, null);
                }
                return new Empty();
            });
        }

        public event EventHandler<Face> ImageReceived;
    }

    public class Face
    {
        public int Emotion { get; set; }
        public double[] Yhat { get; set; }
        public Bitmap Image { get; set; }
    }
}
