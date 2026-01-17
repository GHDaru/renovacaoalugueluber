
import React, { useState } from 'react';

const faqs = [
  {
    q: "Quais os requisitos para alugar?",
    a: "É necessário ter CNH com EAR (Exercício de Atividade Remunerada), ser maior de 21 anos e ter cadastro ativo em aplicativos como Uber ou 99."
  },
  {
    q: "Como funciona o pagamento do caução?",
    a: "O valor de R$ 950,00 deve ser pago no ato da retirada do veículo. Este valor é caucionado para eventuais multas ou danos e devolvido conforme contrato após a entrega do carro."
  },
  {
    q: "E se o carro precisar de manutenção?",
    a: "Toda a manutenção preventiva (troca de óleo, filtros, freios) é por nossa conta. Você apenas agenda e traz o veículo em nossa oficina parceira."
  },
  {
    q: "Posso viajar com o carro?",
    a: "A locação é destinada ao trabalho em Curitiba e Região Metropolitana. Viagens para fora do estado devem ser consultadas previamente."
  }
];

export const FAQ: React.FC = () => {
  const [openIdx, setOpenIdx] = useState<number | null>(0);

  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4 max-w-3xl">
        <h2 className="text-3xl md:text-4xl font-bold text-navy text-center mb-12">Dúvidas Frequentes</h2>
        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div key={idx} className="border border-gray-200 rounded-xl overflow-hidden">
              <button 
                onClick={() => setOpenIdx(openIdx === idx ? null : idx)}
                className="w-full flex justify-between items-center p-5 text-left font-bold text-navy hover:bg-gray-50 transition"
              >
                {faq.q}
                <i className={`fas fa-chevron-${openIdx === idx ? 'up' : 'down'} text-gold text-sm`}></i>
              </button>
              {openIdx === idx && (
                <div className="p-5 bg-gray-50 text-gray-600 border-t border-gray-200 animate-fadeIn">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
