import React from 'react';
import { Text, View, Image, FlatList, Dimensions } from 'react-native';
import { styles } from '@/app/(tabs)/styles/index_styles';

// Get screen width for proper carousel rendering
const { width } = Dimensions.get('window');

// Define the type for props
interface CarouselProps {
  title: string; // Title of the section
  subtitle: string; // Subtitle (Accent title)
  data: Array<{ id: string; image: any; caption: string }>; // Carousel items
}

const Carousel: React.FC<CarouselProps> = ({ title, subtitle, data }) => {
  return (
    <View style={styles.carouselSection}>
      {/* Section Title */}
      <View style={styles.sectionTitleWrapper}>
        <Text style={styles.sectionTitle}>{title}</Text>
        <Text style={styles.sectionTitleAccent}>{subtitle}</Text>
      </View>

      {/* Carousel */}
      <FlatList
        data={data}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={{ width }}>
            <Image source={item.image} style={styles.carouselImage} resizeMode="cover" />
            <Text style={styles.carouselCaption}>{item.caption}</Text>
          </View>
        )}
      />
    </View>
  );
};

export default Carousel;
