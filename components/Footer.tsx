'use client'

import React from 'react'
import Link from 'next/link'
import { Package, Mail, Phone, MapPin } from 'lucide-react'
import { SITE_CONTACT } from '@/lib/site-config'

export function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="mt-auto w-full bg-gradient-to-r from-blue-100 via-indigo-50 to-violet-100 border-t border-indigo-200 text-slate-700">
      <div className="container mx-auto px-4 py-10 md:py-12 max-w-6xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-10">
          {/* Marque / À propos */}
          <div>
            <Link href="/" className="inline-flex items-center gap-2 mb-4">
              <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-blue-400 to-purple-400 flex items-center justify-center shadow-md">
                <Package className="h-4 w-4 text-white" />
              </div>
              <span className="font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                CBIR E-Commerce
              </span>
            </Link>
            <p className="text-sm text-slate-600">
              Recherche visuelle de produits par image ou par texte. Trouvez en un clic des articles similaires.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <h3 className="font-semibold text-indigo-800 mb-4 text-sm uppercase tracking-wide">Navigation</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Accueil
                </Link>
              </li>
              <li>
                <Link href="/" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Boutique
                </Link>
              </li>
              <li>
                <Link href="/" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Produits
                </Link>
              </li>
              <li>
                <Link href="/cart" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Panier
                </Link>
              </li>
            </ul>
          </div>

          {/* Informations légales */}
          <div>
            <h3 className="font-semibold text-indigo-800 mb-4 text-sm uppercase tracking-wide">Informations</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/mentions-legales" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Mentions légales
                </Link>
              </li>
              <li>
                <Link href="/cgv" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  CGV
                </Link>
              </li>
              <li>
                <Link href="/confidentialite" className="text-sm text-slate-600 hover:text-indigo-700 transition-colors">
                  Politique de confidentialité
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold text-indigo-800 mb-4 text-sm uppercase tracking-wide">Contact</h3>
            <ul className="space-y-3 text-sm text-slate-600">
              <li className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-indigo-600 shrink-0" />
                <a href={`mailto:${SITE_CONTACT.email}`} className="hover:text-indigo-700 transition-colors">
                  {SITE_CONTACT.email}
                </a>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-indigo-600 shrink-0" />
                <a href={`tel:${SITE_CONTACT.phone.replace(/\s/g, '')}`} className="hover:text-indigo-700 transition-colors">
                  {SITE_CONTACT.phone}
                </a>
              </li>
              <li className="flex items-start gap-2">
                <MapPin className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                <span>{SITE_CONTACT.location}</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Réseaux sociaux */}
        <div className="mt-8 pt-8 border-t border-indigo-200/60 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <a
              href="https://facebook.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/80 text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800 transition-colors"
              aria-label="Facebook"
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
            </a>
            <a
              href="https://instagram.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/80 text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800 transition-colors"
              aria-label="Instagram"
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073z" />
              </svg>
            </a>
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white/80 text-indigo-600 hover:bg-indigo-100 hover:text-indigo-800 transition-colors"
              aria-label="Twitter"
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </a>
          </div>
          <p className="text-sm text-slate-600">
            © {currentYear} CBIR E-Commerce. Tous droits réservés.
          </p>
        </div>
      </div>
    </footer>
  )
}
