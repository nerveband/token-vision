/**
 * Original TypeScript Implementation
 * This file serves as a reference for the Python port of the Image Token Calculator.
 * It contains the original React-based implementation that we're converting to a Python library.
 */

import React, { useState, useCallback } from 'react';
import { Upload } from 'lucide-react';

const MODELS = {
  claude: {
    name: 'Claude',
    maxImages: 3000,
    models: {
      'claude-3-sonnet': {
        name: 'Claude 3.5 Sonnet',
        inputRate: 0.003,
        outputRate: 0.015
      },
      'claude-3-haiku': {
        name: 'Claude 3.5 Haiku',
        inputRate: 0.0008,
        outputRate: 0.004
      },
      'claude-3-opus': {
        name: 'Claude 3 Opus',
        inputRate: 0.015,
        outputRate: 0.075
      }
    }
  },
  openai: {
    name: 'OpenAI',
    maxImages: 1,
    models: {
      'gpt-4-vision': {
        name: 'GPT-4V',
        inputRate: 0.01
      },
      'gpt-4o': {
        name: 'GPT-4o',
        inputRate: 0.00250
      }
    }
  },
  gemini: {
    name: 'Google Gemini',
    maxImages: 3000,
    models: {
      'gemini-1.5-pro': {
        name: 'Gemini 1.5 Pro',
        inputRate: 0.00125,
        outputRate: 0.005
      },
      'gemini-1.5-flash': {
        name: 'Gemini 1.5 Flash',
        inputRate: 0.000075,
        outputRate: 0.0003
      }
    }
  }
};

const ImageTokenCalculator = () => {
  const [platform, setPlatform] = useState('claude');
  const [model, setModel] = useState('claude-3-sonnet');
  const [dimensions, setDimensions] = useState({ width: 1024, height: 1024 });
  const [detail, setDetail] = useState('high');
  const [dragActive, setDragActive] = useState(false);
  const [imageCount, setImageCount] = useState(1);

  const calculateTokens = (width, height, detail) => {
    if (platform === 'claude') {
      if (width * height <= 384 * 384) {
        return 258;
      }
      const tileSize = Math.min(Math.max(256, Math.min(width, height) / 1.5), 768);
      const tilesX = Math.ceil(width / tileSize);
      const tilesY = Math.ceil(height / tileSize);
      return tilesX * tilesY * 258;
    }
    
    if (detail === 'low') return 85;
    
    let scaledWidth = width;
    let scaledHeight = height;
    if (width > 2048 || height > 2048) {
      const scale = Math.min(2048 / width, 2048 / height);
      scaledWidth = Math.floor(width * scale);
      scaledHeight = Math.floor(height * scale);
    }
    
    const shortestSide = Math.min(scaledWidth, scaledHeight);
    const scale = 768 / shortestSide;
    scaledWidth = Math.floor(scaledWidth * scale);
    scaledHeight = Math.floor(scaledHeight * scale);
    
    const tilesX = Math.ceil(scaledWidth / 512);
    const tilesY = Math.ceil(scaledHeight / 512);
    const totalTiles = tilesX * tilesY;
    
    return totalTiles * 170 + 85;
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const file = e.dataTransfer?.files[0] || e.target.files[0];
    if (!file || !file.type.startsWith('image/')) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => {
        setDimensions({ width: img.width, height: img.height });
      };
      img.src = event.target.result as string;
    };
    reader.readAsDataURL(file);
  }, []);

  const handleDimensionChange = (dim, value) => {
    const newValue = Math.max(1, parseInt(value) || 1);
    setDimensions(prev => ({ ...prev, [dim]: newValue }));
  };

  const handlePlatformChange = (newPlatform) => {
    setPlatform(newPlatform);
    setModel(Object.keys(MODELS[newPlatform].models)[0]);
    setImageCount(1);
  };

  const tokensPerImage = calculateTokens(dimensions.width, dimensions.height, detail);
  const totalTokens = tokensPerImage * imageCount;
  const selectedModel = MODELS[platform].models[model];
  const inputCost = totalTokens * selectedModel.inputRate / 1000000;
  const outputCost = selectedModel.outputRate ? totalTokens * selectedModel.outputRate / 1000000 : 0;

  return (
    <div className="p-6 max-w-2xl mx-auto bg-white rounded-lg shadow">
      <div className="mb-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Platform</label>
          <div className="grid grid-cols-3 gap-2">
            {Object.entries(MODELS).map(([key, value]) => (
              <button
                key={key}
                onClick={() => handlePlatformChange(key)}
                className={`p-2 text-sm border rounded ${
                  platform === key ? 'bg-blue-500 text-white' : 'hover:bg-gray-50'
                }`}
              >
                {value.name}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Model</label>
          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-2 border rounded"
          >
            {Object.entries(MODELS[platform].models).map(([key, value]) => (
              <option key={key} value={key}>{value.name}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-1">Width (px)</label>
          <input
            type="number"
            value={dimensions.width}
            onChange={(e) => handleDimensionChange('width', e.target.value)}
            className="w-full p-2 border rounded"
            min="1"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Height (px)</label>
          <input
            type="number"
            value={dimensions.height}
            onChange={(e) => handleDimensionChange('height', e.target.value)}
            className="w-full p-2 border rounded"
            min="1"
          />
        </div>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium mb-1">
          Number of Images (max {MODELS[platform].maxImages})
        </label>
        <div className="flex gap-4 items-center">
          <input
            type="range"
            min="1"
            max={MODELS[platform].maxImages}
            value={imageCount}
            onChange={(e) => setImageCount(parseInt(e.target.value))}
            className="w-full"
          />
          <input
            type="number"
            value={imageCount}
            onChange={(e) => setImageCount(Math.min(Math.max(1, parseInt(e.target.value) || 1), MODELS[platform].maxImages))}
            className="w-20 p-2 border rounded"
            min="1"
            max={MODELS[platform].maxImages}
          />
        </div>
      </div>

      {platform === 'openai' && (
        <div className="mb-6">
          <label className="block text-sm font-medium mb-1">Detail Level</label>
          <select
            value={detail}
            onChange={(e) => setDetail(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="high">High</option>
            <option value="low">Low</option>
          </select>
        </div>
      )}

      <div 
        className={`relative border-2 border-dashed rounded-lg p-8 mb-6 text-center ${
          dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
        onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); setDragActive(true); }}
        onDragLeave={(e) => { e.preventDefault(); e.stopPropagation(); setDragActive(false); }}
        onDrop={handleDrop}
      >
        <div className="pointer-events-none">
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2">Drag & drop an image or click to upload</p>
        </div>
        <input
          type="file"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          accept="image/*"
          onChange={handleDrop}
          onClick={(e) => e.stopPropagation()}
        />
      </div>

      <div className="text-center p-4 bg-gray-50 rounded-lg space-y-2">
        <p className="text-lg font-semibold">Tokens per image: {tokensPerImage}</p>
        <p className="text-lg font-semibold">Total tokens: {totalTokens}</p>
        <p className="text-lg font-semibold">
          Cost: ${inputCost.toFixed(6)} (input)
          {outputCost > 0 && ` + $${outputCost.toFixed(6)} (output)`}
        </p>
        <p className="text-lg font-semibold">
          Total cost: ${(inputCost + outputCost).toFixed(6)}
        </p>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        <p>Common sizes:</p>
        <div className="grid grid-cols-2 gap-2 mt-2">
          {[
            { name: "Square", w: 1024, h: 1024 },
            { name: "Wide", w: 1920, h: 1080 },
            { name: "Portrait", w: 768, h: 1024 },
            { name: "Banner", w: 2048, h: 512 }
          ].map(size => (
            <button
              key={size.name}
              onClick={() => setDimensions({ width: size.w, height: size.h })}
              className="p-2 text-sm border rounded hover:bg-gray-50"
            >
              {size.name} ({size.w}x{size.h})
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ImageTokenCalculator; 