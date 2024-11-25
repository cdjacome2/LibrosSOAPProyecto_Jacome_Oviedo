using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceModel;

namespace LibrosSOAPServidor
{
    public class LibroService : ILibroService
    {
        private LibrosDBEntities db = new LibrosDBEntities();
        public List<Libro> GetLibros()
        {
            return db.Libros.Select(dbLibro => new Libro
            {
                Id = dbLibro.Id,
                Titulo = dbLibro.Titulo,
                Autor = dbLibro.Autor,
                Año = dbLibro.Año
            }).ToList(); 
        }
        public Libro GetLibroById(int id)
        {
            var dbLibro = db.Libros.Find(id);
            if (dbLibro == null)
            {
                throw new FaultException($"El libro con ID {id} no existe en la base de datos.");
            }
            return new Libro
            {
                Id = dbLibro.Id,
                Titulo = dbLibro.Titulo,
                Autor = dbLibro.Autor,
                Año = dbLibro.Año
            };
        }
        public void AddLibro(Libro libro)
        {
            if (string.IsNullOrWhiteSpace(libro.Titulo) || string.IsNullOrWhiteSpace(libro.Autor))
            {
                throw new FaultException("El título y el autor no pueden estar vacíos.");
            }
            if (libro.Año <= 0)
            {
                throw new FaultException("El año debe ser mayor a cero.");
            }

            var dbLibro = new Libros
            {
                Titulo = libro.Titulo,
                Autor = libro.Autor,
                Año = libro.Año
            };
            db.Libros.Add(dbLibro);
            db.SaveChanges();
        }
        public void UpdateLibro(Libro libro)
        {
            var existing = db.Libros.Find(libro.Id);
            if (existing == null)
            {
                throw new FaultException($"El libro con ID {libro.Id} no existe en la base de datos.");
            }
            existing.Titulo = libro.Titulo;
            existing.Autor = libro.Autor;
            existing.Año = libro.Año;
            db.SaveChanges();
        }
        public void DeleteLibro(int id)
        {
            var libro = db.Libros.Find(id);
            if (libro == null)
            {
                throw new FaultException($"El libro con ID {id} no existe en la base de datos.");
            }
            db.Libros.Remove(libro);
            db.SaveChanges();
        }
    }
}
