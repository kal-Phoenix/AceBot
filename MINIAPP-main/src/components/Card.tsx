import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export function Card({ children, className = '', onClick, hoverable = false }: CardProps) {
  const hoverClasses = hoverable ? 'hover:shadow-xl hover:-translate-y-0.5 cursor-pointer' : '';

  return (
    <div
      onClick={onClick}
      className={`bg-white dark:bg-gray-800 rounded-xl shadow-md transition-all ${hoverClasses} ${className}`}
    >
      {children}
    </div>
  );
}
