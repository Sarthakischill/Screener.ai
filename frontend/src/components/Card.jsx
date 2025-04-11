import React from 'react';

export default function Card({ title, children, footer, className = '' }) {
  return (
    <div className={`bg-white shadow-sm rounded-lg overflow-hidden ${className}`}>
      {title && (
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg font-medium leading-6 text-gray-900">{title}</h3>
        </div>
      )}
      <div className="px-4 py-5 sm:p-6">{children}</div>
      {footer && <div className="px-4 py-4 sm:px-6 bg-gray-50">{footer}</div>}
    </div>
  );
} 