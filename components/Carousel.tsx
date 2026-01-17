
import React, { useState } from 'react';

interface CarouselProps {
  images: string[];
  alt: string;
}

export const Carousel: React.FC<CarouselProps> = ({ images, alt }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToPrevious = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? images.length - 1 : prevIndex - 1
    );
  };

  const goToNext = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === images.length - 1 ? 0 : prevIndex + 1
    );
  };

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  return (
    <div className="relative w-full h-48 overflow-hidden rounded-t-2xl group">
      {/* Main Image */}
      <div className="relative w-full h-full">
        <img 
          src={images[currentIndex]} 
          alt={`${alt} - ${currentIndex + 1}`}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Previous Button */}
      <button
        onClick={goToPrevious}
        className="absolute left-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full w-8 h-8 flex items-center justify-center transition opacity-0 group-hover:opacity-100"
        aria-label="Imagem anterior"
      >
        <i className="fas fa-chevron-left text-sm"></i>
      </button>

      {/* Next Button */}
      <button
        onClick={goToNext}
        className="absolute right-2 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full w-8 h-8 flex items-center justify-center transition opacity-0 group-hover:opacity-100"
        aria-label="Próxima imagem"
      >
        <i className="fas fa-chevron-right text-sm"></i>
      </button>

      {/* Dots Indicator */}
      <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-2">
        {images.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`w-2 h-2 rounded-full transition ${
              index === currentIndex 
                ? 'bg-white w-4' 
                : 'bg-white/50 hover:bg-white/70'
            }`}
            aria-label={`Ir para imagem ${index + 1}`}
          />
        ))}
      </div>

      {/* Image Label */}
      <div className="absolute top-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded">
        {currentIndex === 0 ? 'Carro' : currentIndex === 1 ? 'Interior' : 'Painel'}
      </div>
    </div>
  );
};
