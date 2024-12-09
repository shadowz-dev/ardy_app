
import React from 'react';
import { Text, View, ScrollView, Image, FlatList, Dimensions, SafeAreaView } from 'react-native';
import { styles } from './styles/index_styles';
import { Rating } from 'react-native-ratings';
import Carousel from '@/components/carousel';

// Mock data for carousel images
const carouselImages = [
    {
      id: '1',
      image: { uri: 'https://via.placeholder.com/400x200.png?text=Latest+Construction+Projects' },
      caption: 'Latest Consultant joined',
    },
    {
      id: '2',
      image: { uri: 'https://via.placeholder.com/400x200.png?text=Modern+Interior+Designs' },
      caption: 'Modern Interior Designs',
    },
    {
      id: '3',
      image: { uri: 'https://via.placeholder.com/400x200.png?text=Smart+Home+Innovations' },
      caption: 'Smart Home Innovations',
    },
  ];

export default function OffersScreen() {
    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={styles.container}>
                <Carousel
                title= "Latest"
                subtitle="Offers!"
                data={carouselImages}
                />
            </ScrollView>
        </SafeAreaView>
      );
    }
    
