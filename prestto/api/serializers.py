from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=True)
    phone_number = serializers.CharField(validators=[validate_phone_number], required=True)
    gender = serializers.CharField(validators=[validate_gender], required=False)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="This username is in use, please try a different one")])
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())], max_length=32)
    referee = serializers.CharField(required=False)  # referral code of the affiliate marketer
    password = serializers.CharField(min_length=8, write_only=True)

    # The client should not be able to send a token or points along with a registration
    # request. Making them read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    email_token = serializers.CharField(max_length=255, read_only=True)
    points = serializers.IntegerField(read_only=True)
    referral_code = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        serializer.save() calls this function
        """
        token = token_generator()
        referral_code = generate_referral_code()
        validated_data['email_token'] = token
        validated_data['referral_code'] = referral_code
        ref_code = validated_data.get("referee", None)
        if ref_code:
            try:
                referee = AffiliateInfo.objects.get(user__referral_code=ref_code)
                referee.total_signups += 1
                referee.save()
                validated_data['referee'] = ref_code
            except [AffiliateInfo.DoesNotExist, Exception] as e:
                print(e, "Error for affiliate processing....................")
                pass
        user = User.objects.create_user(**validated_data)

        # create an affiliate profile for the user
        affiliate_info = AffiliateInfo.objects.create(user=user)

        name = user.fullname
        email = validated_data.get("email")
        print("I'm about to send a mail initiation...............................................")
        send_email_verification_pin(email=email, pin=token, name=name)

        return user

    # def validate_email_address(self, email, token):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number',
                  'fullname', 'institution', 'date_of_birth', 'gender', 'token', 'points', 'image', 'email_token',
                  'referee', 'referral_code')
