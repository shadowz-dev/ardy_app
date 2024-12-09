import { StyleSheet, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width * 0.3; // Adjusted card width for symmetry
const FULL_WIDTH = width; // Full width for carousels
const SPACING = 10; // Consistent spacing

export default function Placeholder() {
  return null;
}

export const styles = StyleSheet.create({
  container: {
    backgroundColor: '#2d363b',
    paddingBottom: 15, // Reduced padding bottom
    paddingHorizontal: 0, // Full-width alignment
  },

  // Section Titles
  sectionTitleWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5, // Reduced bottom margin
    marginTop: 5, // Consistent top margin
    paddingHorizontal: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
  },
  sectionTitleAccent: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#8ee7e4',
    marginLeft: 5,
  },

  // Stories Section
  sliderSection: {
    marginBottom: 5, // Reduced gap
    marginTop: 5,
  },

  // Carousel Section
  carouselSection: {
    marginBottom: 5, // Reduced bottom spacing
    marginTop: 5,
  },
  carouselItem: {
    width: FULL_WIDTH, // Full width for single images
    borderRadius: 12,
    overflow: 'hidden',
    marginHorizontal: 0,
  },
  carouselImage: {
    width: FULL_WIDTH,
    height: 180,
    resizeMode: 'cover',
  },
  carouselCaption: {
    fontSize: 14,
    fontWeight: '600',
    color: '#ddd',
    textAlign: 'center',
    marginTop: 5,
  },

  // Service Providers and Reviews
  slider: {
    marginTop: 5, // Reduced spacing
    marginBottom: 5,
  },
  card: {
    width: CARD_WIDTH, // Cards fit 3 items fully
    marginHorizontal: SPACING / 2,
    backgroundColor: '#3e444a',
    borderRadius: 12,
    paddingVertical: 12,
    paddingHorizontal: 8,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
  },
  cardText: {
    color: '#fff',
    fontSize: 12,
    textAlign: 'center',
    marginBottom: 8,
  },
  providerLogo: {
    width: 55,
    height: 55,
    borderRadius: 27.5,
    marginBottom: 12,
  },
  stars: {
    backgroundColor: 'transparent', // Added missing style
    marginTop: 15,
    marginBottom: 5,
  },
  ratingContainer: {
    marginBottom: 15,
  },
  username: {
    color: '#ccc',
    fontSize: 11,
    fontStyle: 'italic',
    textAlign: 'center',
  },

  // Services Section
  servicesSection: {
    marginBottom: 5, // Reduced spacing
    marginTop: 10,
    paddingHorizontal: 15,
  },
  serviceCard: {
    backgroundColor: '#3e444a',
    borderRadius: 10,
    padding: 12,
    marginBottom: 12,
    elevation: 2,
  },
  serviceTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 6,
  },
  serviceDescription: {
    fontSize: 13,
    color: '#bbb',
  },

  // Placeholder Text
  placeholder: {
    textAlign: 'center',
    fontSize: 14,
    color: '#aaa',
    marginVertical: 10,
  },
});
