
import React from 'react';

const reviews = [
  {
    name: "Ricardo Silva",
    role: "Motorista Uber Gold",
    text: "Aluguei o Logan e o consumo é excelente. O atendimento da Renovação é nota 10, sempre que precisei de revisão foi muito rápido."
  },
  {
    name: "Marcos Oliveira",
    role: "Motorista 99Pop",
    text: "O melhor preço de Curitiba. O caução não é abusivo e os carros estão sempre novos. Recomendo para quem quer trabalhar sério."
  },
  {
    name: "Ana Paula",
    role: "Motorista Uber Comfort",
    text: "Trabalho com o Cronos deles e meus passageiros elogiam muito o conforto. O suporte pelo WhatsApp resolve tudo na hora."
  }
];

export const Testimonials: React.FC = () => {
  return (
    <section className="py-20 bg-navy text-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Quem dirige com a gente, aprova!</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {reviews.map((rev, idx) => (
            <div key={idx} className="bg-white/5 p-8 rounded-2xl border border-white/10 hover:border-gold transition">
              <div className="text-gold mb-4">
                <i className="fas fa-star"></i>
                <i className="fas fa-star"></i>
                <i className="fas fa-star"></i>
                <i className="fas fa-star"></i>
                <i className="fas fa-star"></i>
              </div>
              <p className="italic text-gray-300 mb-6">"{rev.text}"</p>
              <div>
                <p className="font-bold">{rev.name}</p>
                <p className="text-sm text-gold">{rev.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
