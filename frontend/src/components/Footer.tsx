
import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white pt-16 pb-8">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-12 mb-12">
          <div className="col-span-2">
            <div className="flex items-center space-x-2 mb-6">
              <div className="w-10 h-10 flex items-center justify-center border-2 border-white transform rotate-45 overflow-hidden p-1">
                <span className="text-xl font-black text-white -rotate-45">R</span>
              </div>
              <div className="flex flex-col leading-tight">
                <span className="font-bold text-lg tracking-wider">RENOVAÇÃO</span>
                <span className="text-[8px] font-semibold text-gray-400 uppercase tracking-widest">Locação e Empreendimentos</span>
              </div>
            </div>
            <p className="text-gray-400 max-w-sm mb-6">
              Especialistas em mobilidade para motoristas profissionais. 
              Sua ferramenta de trabalho com o melhor suporte de Curitiba.
            </p>
            <div className="flex space-x-4">
              <a href="#frota" className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-gold hover:text-navy transition">
                <i className="fas fa-car"></i>
              </a>
              <a href="#planos" className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-gold hover:text-navy transition">
                <i className="fas fa-tag"></i>
              </a>
            </div>
          </div>
          
          <div>
            <h4 className="text-lg font-bold mb-6 text-gold">Contatos</h4>
            <ul className="space-y-4 text-gray-400">
              <li className="flex items-start">
                <i className="fas fa-phone-alt mt-1 mr-3 text-gold"></i>
                <span>(41) 99257-5775</span>
              </li>
              <li className="flex items-start">
                <i className="fab fa-whatsapp mt-1 mr-3 text-gold text-lg"></i>
                <span>(41) 99257-5775</span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-envelope mt-1 mr-3 text-gold"></i>
                <span>contato@renovacaolocacao.com.br</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-bold mb-6 text-gold">Localização</h4>
            <ul className="space-y-4 text-gray-400">
              <li className="flex items-start">
                <i className="fas fa-map-marker-alt mt-1 mr-3 text-gold"></i>
                <span>Atendimento em Curitiba e Região Metropolitana</span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-clock mt-1 mr-3 text-gold"></i>
                <span>Segunda a Sexta: 08:30 - 18:00<br/>Sábado: 09:00 - 12:00</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-white/10 pt-8 text-center text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} Renovação Locação e Empreendimentos. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
};
