// Import gambar dari folder assets
import borobudur from '../assets/images/borobudur.jpg'
import prambanan from '../assets/images/prambanan.jpg'
import malioboro from '../assets/images/malioboro.jpg'
import parangtritis from '../assets/images/parangtritis.jpg'
import tamansari from '../assets/images/tamansari.jpg'
import merapi from '../assets/images/gunungmerapi.jpg'

export const destinations = [{
        id: 1,
        name: 'Candi Borobudur',
        country: 'MAGELANG',
        price: 'Rp 50.000',
        rating: '4.9',
        reviews: '25.3k',
        description: 'Candi Buddha terbesar di dunia yang dibangun pada abad ke-9 Masehi. Terdiri dari 10 tingkatan dengan 2.672 panel relief dan 504 arca Buddha.',
        image: borobudur, // Menggunakan gambar yang diimport
        location: 'Magelang, Jawa Tengah'
    },
    {
        id: 2,
        name: 'Candi Prambanan',
        country: 'SLEMAN',
        price: 'Rp 50.000',
        rating: '4.8',
        reviews: '18.7k',
        description: 'Candi Hindu terbesar di Indonesia dengan arsitektur yang megah dan menjulang tinggi. Dibangun pada abad ke-9 Masehi.',
        image: prambanan,
        location: 'Sleman, Yogyakarta'
    },
    {
        id: 3,
        name: 'Malioboro',
        country: 'YOGYAKARTA',
        price: 'Gratis',
        rating: '4.7',
        reviews: '32.1k',
        description: 'Jalan ikonik di Yogyakarta yang terkenal dengan suasana malam yang ramai, street food, dan pusat oleh-oleh khas Jogja.',
        image: malioboro,
        location: 'Yogyakarta, DIY'
    },
    {
        id: 4,
        name: 'Pantai Parangtritis',
        country: 'BANTUL',
        price: 'Rp 15.000',
        rating: '4.6',
        reviews: '15.8k',
        description: 'Pantai eksotis dengan pasir hitam dan ombak besar. Tempat yang populer untuk menikmati sunset dan wisata religi.',
        image: parangtritis,
        location: 'Bantul, Yogyakarta'
    },
    {
        id: 5,
        name: 'Taman Sari',
        country: 'YOGYAKARTA',
        price: 'Rp 15.000',
        rating: '4.5',
        reviews: '12.4k',
        description: 'Bekas taman keraton yang indah dengan kolam renang dan lorong bawah tanah. Dibangun pada masa Sultan Hamengkubuwono I.',
        image: tamansari,
        location: 'Yogyakarta, DIY'
    },
    {
        id: 6,
        name: 'Gunung Merapi',
        country: 'SLEMAN',
        price: 'Rp 350.000',
        rating: '4.8',
        reviews: '9.6k',
        description: 'Gunung berapi aktif terindah di Indonesia dengan pemandangan sunrise yang spektakuler dan petualangan jeep yang seru.',
        image: merapi,
        location: 'Sleman, Yogyakarta'
    }
]