
import React from 'react';

export const WhatsAppButton: React.FC = () => {
  return (
    <a 
      href="https://wa.me/5541992575775" 
      target="_blank" 
      rel="noopener noreferrer"
      className="fixed bottom-6 right-6 z-[999] bg-green-500 text-white w-16 h-16 rounded-full shadow-2xl flex items-center justify-center text-3xl hover:bg-green-600 hover:scale-110 transition-all duration-300 animate-bounce-slow"
      aria-label="Contato via WhatsApp"
    >
      <i className="fab fa-whatsapp"></i>
      <span className="absolute -top-2 -left-2 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded-full border-2 border-white">
        1
      </span>
    </a>
  );
};
