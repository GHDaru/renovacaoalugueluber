
import React from 'react';

const benefits = [
  {
    icon: "fa-road",
    title: "KM Livre",
    desc: "Rode sem limites e sem preocupações com a quilometragem no fim do dia."
  },
  {
    icon: "fa-shield-halved",
    title: "Seguro Total",
    desc: "Sua proteção é nossa prioridade. Cobertura total com franquia facilitada."
  },
  {
    icon: "fa-screwdriver-wrench",
    title: "Manutenção Inclusa",
    desc: "Manutenções preventivas e corretivas inclusas para você nunca ficar parado."
  },
  {
    icon: "fa-bolt",
    title: "Burocracia Zero",
    desc: "Processo de aprovação rápido para você começar a dirigir hoje mesmo."
  }
];

export const Features: React.FC = () => {
  return (
    <section id="beneficios" className="py-20 bg-white">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-navy mb-4">Por que escolher a Renovação?</h2>
        <p className="text-gray-600 mb-16 max-w-2xl mx-auto">Oferecemos as melhores condições para motoristas de aplicativos em Curitiba e Região Metropolitana.</p>
        
        <div className="grid md:grid-cols-4 gap-8">
          {benefits.map((item, idx) => (
            <div key={idx} className="p-8 rounded-2xl bg-gray-50 hover:bg-white hover:shadow-2xl transition duration-300 group">
              <div className="w-16 h-16 bg-navy text-gold rounded-xl flex items-center justify-center mb-6 mx-auto transform group-hover:scale-110 transition">
                <i className={`fas ${item.icon} text-2xl`}></i>
              </div>
              <h3 className="text-xl font-bold text-navy mb-3">{item.title}</h3>
              <p className="text-gray-600 text-sm leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
