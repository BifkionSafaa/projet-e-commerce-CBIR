/**
 * Coordonnées de contact du site.
 * Remplacez par votre vrai email et numéro de téléphone.
 * Vous pouvez aussi utiliser les variables d'environnement :
 * NEXT_PUBLIC_CONTACT_EMAIL et NEXT_PUBLIC_CONTACT_PHONE dans .env.local
 */
export const SITE_CONTACT = {
  email: process.env.NEXT_PUBLIC_CONTACT_EMAIL ?? 'contact@cbir-ecommerce.com',
  phone: process.env.NEXT_PUBLIC_CONTACT_PHONE ?? '+212 537 00 00 00',
  location: 'Maroc',
}
