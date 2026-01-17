
import React from 'react';
import { Carousel } from './Carousel';

const cars = [
  {
    name: "Renault Logan",
    category: "Uber X / Comfort",
    images: [
      "/images/logancarro.jpg",
      "/images/loganinterior.jpg",
      "/images/loganpainel.jpg"
    ],
    features: ["4 Portas", "Ar Condicionado", "Porta-Malas Grande", "Econômico"]
  },
  {
    name: "Toyota Etios",
    category: "Uber X / Comfort",
    images: [
      "/images/etioscarro.jpg",
      "/images/Etiosinterior.jpg",
      "/images/Etiospainel.jpg"
    ],
    features: ["Conforto Premium", "Multimídia", "Direção Elétrica", "Confiável"]
  }
];

export const Fleet: React.FC = () => {
  return (
    <section id="frota" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-navy text-center mb-12">Conheça Nossa Frota</h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {cars.map((car, idx) => (
            <div key={idx} className="bg-gray-50 rounded-2xl overflow-hidden shadow-lg border border-gray-100 group">
              <Carousel images={car.images} alt={car.name} />
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-navy">{car.name}</h3>
                    <span className="text-xs font-bold text-gold uppercase">{car.category}</span>
                  </div>
                  <div className="bg-green-100 text-green-700 text-[10px] font-black px-2 py-1 rounded">DISPONÍVEL</div>
                </div>
                <ul className="space-y-2 mb-6">
                  {car.features.map((f, i) => (
                    <li key={i} className="text-sm text-gray-600 flex items-center">
                      <i className="fas fa-chevron-right text-[10px] text-gold mr-2"></i> {f}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
