
import React from 'react';

export const Pricing: React.FC = () => {
  return (
    <section id="planos" className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row">
          <div className="md:w-2/5 bg-navy text-white p-10 flex flex-col justify-center">
            <span className="text-gold font-bold uppercase tracking-widest text-sm mb-2">Oferta Exclusiva</span>
            <h2 className="text-4xl font-black mb-6">Plano Uber X / Comfort</h2>
            <div className="space-y-4 mb-8">
              <div className="flex items-center space-x-3">
                <i className="fas fa-check-circle text-gold"></i>
                <span className="font-semibold text-lg">Caução: R$ 1.500,00</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-check-circle text-gold"></i>
                <span className="font-semibold text-lg">Diária: R$ 120,00</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-check-circle text-gold"></i>
                <span className="font-semibold text-lg">Seguro Total</span>
              </div>
              <div className="flex items-center space-x-3">
                <i className="fas fa-check-circle text-gold"></i>
                <span className="font-semibold text-lg">KM Livre</span>
              </div>
            </div>
            <div className="flex items-center p-3 bg-red-600 bg-opacity-20 border border-red-500 rounded-lg text-red-200">
              <i className="fas fa-ban mr-3"></i>
              <span className="text-xs font-bold uppercase">Proibido Fumar no Veículo</span>
            </div>
          </div>
          
          <div className="md:w-3/5 p-10 flex flex-col justify-between">
            <div>
              <h3 className="text-2xl font-bold text-navy mb-4">Comece a Faturar Agora</h3>
              <p className="text-gray-600 mb-8">
                Nossos carros são revisados e atendem a todos os requisitos da Uber e 99. 
                Oferecemos condições competitivas e veículos de qualidade para sua operação.
              </p>
              
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="bg-gray-50 p-4 rounded-xl">
                  <p className="text-gray-500 text-xs font-bold uppercase mb-1">Pagamento</p>
                  <p className="text-navy font-bold">Semanal / Pix</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-xl">
                  <p className="text-gray-500 text-xs font-bold uppercase mb-1">Caução</p>
                  <p className="text-navy font-bold">Devolutivo</p>
                </div>
              </div>
            </div>
            
            <a 
              href="https://wa.me/5541992575775" 
              className="w-full bg-gold text-navy text-center font-black py-4 rounded-xl shadow-lg hover:bg-yellow-500 transition text-xl"
            >
              RESERVAR VEÍCULO AGORA
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};
