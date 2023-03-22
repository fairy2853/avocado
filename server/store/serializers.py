#!/usr/bin/python
#
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from rest_framework import serializers

from store.models import Product, SiteConfig, Testimonial


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discount_price",
            "active",
            "discount_percent",
            "discount_saving",
            "inventory_count",
            "image",
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "id",
            "product_id",
            "reviewer_name",
            "reviewer_location",
            "rating",
            "summary",
            "description",
        ]


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = [
            "active",
            "color_primary",
            "color_secondary",
            "color_action",
            "color_action_text",
            "site_name",
            "site_name_font",
            "site_name_color",
            "base_font",
        ]

    
class CartPaymentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=["collect"])


class CartCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField()

class CartItemSerializer(serializers.Serializer):
    def valid_product(value):
        try:
            _ = Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f'Product {value} not found')

    id = serializers.IntegerField(validators=[valid_product])
    countRequested = serializers.IntegerField(required=True)
    countFulfilled = serializers.IntegerField(required=False)

    def validate(self, data):
        product = Product.objects.get(pk=data["id"])
        requested = data["countRequested"]
        if product.inventory_count < requested:
            raise serializers.ValidationError(f'Insufficient product to fulfil request')
        return data

class CartSerializer(serializers.Serializer):
    customer = CartCustomerSerializer(required=True)
    payment = CartPaymentSerializer(required=True)
    items = CartItemSerializer(many=True)

class CheckoutSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    status = serializers.CharField()
