
import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="w-12 h-12 flex items-center justify-center border-2 border-navy transform rotate-45 overflow-hidden p-1">
            <span className="text-2xl font-black text-navy -rotate-45">R</span>
          </div>
          <div className="flex flex-col leading-tight">
            <span className="font-bold text-lg tracking-wider text-navy">RENOVAÇÃO</span>
            <span className="text-[10px] font-semibold text-gray-500 uppercase tracking-widest">Locação e Empreendimentos</span>
          </div>
        </div>
        
        <nav className="hidden md:flex space-x-8 font-semibold text-gray-600">
          <a href="#beneficios" className="hover:text-gold transition">Benefícios</a>
          <a href="#planos" className="hover:text-gold transition">Planos</a>
          <a href="#frota" className="hover:text-gold transition">Frota</a>
        </nav>

        <a 
          href="https://wa.me/5541992575775" 
          target="_blank" 
          className="bg-navy text-white px-6 py-2 rounded-full font-bold hover:bg-gray-800 transition shadow-lg hidden sm:block"
        >
          CONTATO
        </a>
      </div>
    </header>
  );
};
