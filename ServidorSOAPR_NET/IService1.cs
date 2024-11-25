using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;


namespace LibrosSOAPServidor
{
    [ServiceContract]
    public interface ILibroService
    {
        [OperationContract]
        List<Libro> GetLibros();

        [OperationContract]
        Libro GetLibroById(int id);

        [OperationContract]
        void AddLibro(Libro libro);

        [OperationContract]
        void UpdateLibro(Libro libro);

        [OperationContract]
        void DeleteLibro(int id);
    }

    [DataContract]
    public class Libro
    {
        [DataMember]
        public int Id { get; set; }

        [DataMember]
        public string Titulo { get; set; }

        [DataMember]
        public string Autor { get; set; }

        [DataMember]
        public int Año { get; set; }
    }
}
