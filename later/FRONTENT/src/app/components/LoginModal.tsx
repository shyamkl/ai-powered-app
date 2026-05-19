import { X, User, Briefcase } from 'lucide-react';
import { useState } from 'react';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'customer' | 'vendor';
}

export function LoginModal({ isOpen, onClose, type }: LoginModalProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="text-center mb-6">
          {type === 'customer' ? (
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <User className="w-8 h-8 text-blue-600" />
            </div>
          ) : (
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Briefcase className="w-8 h-8 text-purple-600" />
            </div>
          )}
          <h2 className="text-2xl mb-2">
            {type === 'customer' ? 'Customer Login' : 'Vendor Login'}
          </h2>
          <p className="text-gray-600 text-sm">
            {type === 'customer'
              ? 'Sign in to save favorites and write reviews'
              : 'Access your dashboard and analytics'}
          </p>
        </div>

        <form className="space-y-4">
          <div>
            <label className="block text-sm mb-2 text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="your@email.com"
            />
          </div>

          <div>
            <label className="block text-sm mb-2 text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            className={`w-full py-3 rounded-xl text-white transition-all ${
              type === 'customer'
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg'
                : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:shadow-lg'
            }`}
          >
            Sign In
          </button>

          <div className="text-center">
            <a href="#" className="text-sm text-blue-600 hover:underline">
              Forgot password?
            </a>
          </div>

          <div className="text-center pt-4 border-t border-gray-200">
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <a href="#" className="text-blue-600 hover:underline">
                Sign up
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
