"""Noise generation utilities for privacy preservation"""

import numpy as np


def generate_gaussian_noise(size=1, mu=0, sigma=1):
    """Generate Gaussian (normal) noise"""
    return np.random.normal(mu, sigma, size)


def generate_laplace_noise(size=1, mu=0, scale=1):
    """Generate Laplace noise"""
    return np.random.laplace(mu, scale, size)


def add_noise_to_value(value, noise_type='gaussian', epsilon=0.5):
    """Add privacy-preserving noise to a value"""
    if noise_type == 'gaussian':
        noise = generate_gaussian_noise(sigma=1/epsilon)
    elif noise_type == 'laplace':
        noise = generate_laplace_noise(scale=1/epsilon)
    else:
        noise = 0
    
    return value + noise[0]
