export const getFullImageUrl = (path) => {
    if (!path) return null;

    // If it's already a full URL, return it as-is
    if (path.startsWith('http://') || path.startsWith('https://')) {
        return path;
    }

    // Get the base API URL from environment, fallback to localhost
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    // Remove trailing slash if present
    const base = baseUrl.replace(/\/$/, '');
    // Ensure path starts with a slash
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;

    return `${base}${normalizedPath}`;
};