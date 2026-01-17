
import React from 'react';

export const Hero: React.FC = () => {
  return (
    <section className="relative bg-navy text-white overflow-hidden py-16 md:py-24">
      {/* Background Graphic */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gold opacity-10 transform skew-x-12 translate-x-24"></div>
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <div className="inline-block bg-gold text-navy font-black text-sm px-4 py-1 rounded-full mb-6 animate-pulse">
              PROMOÇÃO DE LANÇAMENTO 🚀
            </div>
            <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">
              O Carro Certo para Você <span className="text-gold">Rodar e Lucrar.</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-300 mb-8 max-w-lg">
              Aluguel de veículos Categoria X e Comfort para Uber em Curitiba. Menos burocracia, mais lucro no seu bolso.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a 
                href="#planos" 
                className="bg-gold text-navy text-center font-bold px-8 py-4 rounded-lg shadow-xl hover:scale-105 transition transform"
              >
                VER PLANOS DISPONÍVEIS
              </a>
              <a 
                href="https://wa.me/5541992575775" 
                className="border-2 border-white text-center font-bold px-8 py-4 rounded-lg hover:bg-white hover:text-navy transition"
              >
                FALAR COM CONSULTOR
              </a>
            </div>
          </div>
          
          <div className="md:w-1/2 relative">
            <div className="relative z-10 transform md:scale-110 lg:translate-x-10">
              <img 
                src="https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&q=80&w=800" 
                alt="Renault Logan 2018" 
                className="rounded-2xl shadow-2xl"
              />
              <div className="absolute -bottom-6 -left-6 bg-white p-6 rounded-xl shadow-2xl hidden lg:block">
                <p className="text-navy font-black text-3xl">R$ 120</p>
                <p className="text-gray-500 text-xs font-bold uppercase tracking-widest">A partir da diária</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
