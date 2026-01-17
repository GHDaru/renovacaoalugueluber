
import React from 'react';

const cars = [
  {
    name: "Renault Logan",
    category: "Uber X / Comfort",
    img: "https://images.unsplash.com/photo-1630175860333-5131bda75071?auto=format&fit=crop&q=80&w=400",
    features: ["4 Portas", "Ar Condicionado", "Porta-Malas Grande"]
  },
  {
    name: "Fiat Cronos",
    category: "Uber X / Comfort",
    img: "https://images.unsplash.com/photo-1619682817481-e99489121f82?auto=format&fit=crop&q=80&w=400",
    features: ["Econômico", "Conforto Premium", "Multimídia"]
  },
  {
    name: "Volkswagen Voyage",
    category: "Uber X",
    img: "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=400",
    features: ["Direção Hidráulica", "Excelente Desempenho", "Confiável"]
  }
];

export const Fleet: React.FC = () => {
  return (
    <section id="frota" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-navy text-center mb-12">Conheça Nossa Frota</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {cars.map((car, idx) => (
            <div key={idx} className="bg-gray-50 rounded-2xl overflow-hidden shadow-lg border border-gray-100 group">
              <div className="h-48 overflow-hidden">
                <img 
                  src={car.img} 
                  alt={car.name} 
                  className="w-full h-full object-cover group-hover:scale-110 transition duration-500"
                />
              </div>
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
