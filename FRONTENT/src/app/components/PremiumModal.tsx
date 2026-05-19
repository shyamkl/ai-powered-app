import { X, Crown, Check } from 'lucide-react';
import { useState } from 'react';

interface PremiumModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubscribe: () => void;
  userLocation: string;
  isPremiumMember?: boolean;
}

export function PremiumModal({ isOpen, onClose, onSubscribe, userLocation, isPremiumMember = false }: PremiumModalProps) {
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'yearly'>('monthly');

  if (!isOpen) return null;

  const pricing = {
    India: {
      monthly: '₹499',
      yearly: '₹4,999',
      currency: 'INR',
      savings: '₹999'
    },
    Thailand: {
      monthly: '฿299',
      yearly: '฿2,999',
      currency: 'THB',
      savings: '฿589'
    },
    Other: {
      monthly: '$9.99',
      yearly: '$99.99',
      currency: 'USD',
      savings: '$19.89'
    }
  };

  const locationKey = userLocation === 'India' ? 'India' : userLocation === 'Thailand' ? 'Thailand' : 'Other';
  const currentPricing = pricing[locationKey];

  const features = [
    'Extra 20% off on all happy hour deals',
    'Priority table reservations',
    'Exclusive access to premium venues',
    'No ads experience',
    'Early access to new features',
    'Personalized AI recommendations',
    'Access to AR menu previews',
    'Monthly surprise rewards'
  ];

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full my-8 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 bg-white hover:bg-gray-100 text-gray-700 hover:text-gray-900 p-2 rounded-full shadow-lg z-10 transition-all"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Header */}
        <div className="bg-gradient-to-r from-amber-500 to-yellow-500 text-white p-8 rounded-t-3xl text-center">
          <Crown className="w-16 h-16 mx-auto mb-4" />
          <h2 className="text-4xl mb-2">{isPremiumMember ? 'Premium Membership' : 'Go Premium'}</h2>
          <p className="text-lg opacity-90">
            {isPremiumMember ? 'You are enjoying premium benefits!' : 'Unlock exclusive benefits and save more!'}
          </p>
        </div>

        {/* Pricing Toggle */}
        <div className="p-8">
          <div className="flex justify-center mb-8">
            <div className="bg-gray-100 rounded-full p-1 inline-flex">
              <button
                onClick={() => setSelectedPlan('monthly')}
                className={`px-6 py-3 rounded-full transition-all ${
                  selectedPlan === 'monthly'
                    ? 'bg-gradient-to-r from-amber-500 to-yellow-500 text-white shadow-lg'
                    : 'text-gray-700'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setSelectedPlan('yearly')}
                className={`px-6 py-3 rounded-full transition-all relative ${
                  selectedPlan === 'yearly'
                    ? 'bg-gradient-to-r from-amber-500 to-yellow-500 text-white shadow-lg'
                    : 'text-gray-700'
                }`}
              >
                Yearly
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                  Save 17%
                </span>
              </button>
            </div>
          </div>

          {/* Pricing Display */}
          <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-2xl p-8 mb-8 text-center border-2 border-amber-200">
            <div className="text-5xl mb-2">
              {selectedPlan === 'monthly' ? currentPricing.monthly : currentPricing.yearly}
            </div>
            <div className="text-gray-600 text-lg mb-4">
              per {selectedPlan === 'monthly' ? 'month' : 'year'}
            </div>
            {selectedPlan === 'yearly' && (
              <div className="inline-block bg-green-100 text-green-700 px-4 py-2 rounded-full text-sm">
                Save {currentPricing.savings} compared to monthly!
              </div>
            )}
          </div>

          {/* Features List */}
          <div className="mb-8">
            <h3 className="text-xl mb-4 text-center">Premium Features</h3>
            <div className="grid md:grid-cols-2 gap-3">
              {features.map((feature, idx) => (
                <div key={idx} className="flex items-start gap-3">
                  <div className="bg-green-100 rounded-full p-1 mt-0.5">
                    <Check className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-gray-700 text-sm">{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Subscribe Button or Active Status */}
          {isPremiumMember ? (
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-500 rounded-xl p-6 text-center">
              <div className="flex items-center justify-center gap-2 text-green-700 text-xl mb-2">
                <Crown className="w-6 h-6 fill-green-600" />
                <span className="font-semibold">Premium Active</span>
              </div>
              <p className="text-gray-600 mb-4">
                Your subscription: Monthly Plan - {currentPricing.monthly}
              </p>
              <button
                onClick={onClose}
                className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 rounded-xl transition-all"
              >
                Close
              </button>
            </div>
          ) : (
            <>
              <button
                onClick={() => {
                  onSubscribe();
                  onClose();
                }}
                className="w-full bg-gradient-to-r from-amber-500 to-yellow-500 text-white py-4 rounded-xl text-lg hover:shadow-2xl transition-all hover:scale-105"
              >
                Subscribe Now - {selectedPlan === 'monthly' ? currentPricing.monthly : currentPricing.yearly}
              </button>

              <p className="text-center text-gray-500 text-sm mt-4">
                Cancel anytime. No hidden fees.
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
